from bs4 import BeautifulSoup
from calendar import monthrange
from datetime import datetime
import requests
import time


class ScrapeTideForecast:
    def scrape_tide_forecast(self, tide_urls):
        results = {tide_url: [] for tide_url in tide_urls}
        counter = 0

        for url in tide_urls:
            days_remaining_in_month = monthrange(
                datetime.today().year, datetime.today().month)[1] - datetime.today().day
            while days_remaining_in_month >= 0:
                if counter == 0:
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    result = {}
                    today = soup.find('h3')
                    result['Day'] = today.text.split('day ')[1]
                    sun_info = str(soup.select('[class~=tide-header-summary]'))
                    result['Sunrise'] = sun_info.split('Sunrise is at  ', 6)[
                        1].split(' and')[0]
                    result['Sunset'] = sun_info.split('Sunrise is at  ', 6)[
                        1].split('at  ')[1].split('.')[0]
                    self.iterate_tide_table(soup, result, counter)
                    results[url].append(result)
                    counter += 1
                    days_remaining_in_month -= 1
                else:
                    result = {}
                    self.iterate_sun_table(soup, result, counter)
                    self.iterate_tide_table(soup, result, counter)
                    results[url].append(result)
                    counter += 1
                    days_remaining_in_month -= 1
            counter = 0
            continue

        return results

    def iterate_sun_table(self, soup, result, counter):
        sun_table_list = soup.findAll(
            'table', {'class': 'not-in-print tide-day__sun-moon'})
        sun_rows = sun_table_list[counter - 1].findAll('tr')
        sun_table_data = []
        for row in sun_rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            sun_table_data.append([ele for ele in cols if ele])
        result['Sunrise'] = sun_table_data[0][0].split(': ')[1]
        result['Sunset'] = sun_table_data[0][1].split(': ')[1]

        return result

    def iterate_tide_table(self, soup, result, counter):
        table_list = soup.findAll('table', {'class': 'tide-day-tides'})

        rows = table_list[counter].findAll('tr')
        table_data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            table_data.append([ele for ele in cols if ele])
        for tab in table_data:
            if 'Low Tide' in tab:
                day_low_tide_time = tab[1].split('(')[0]
                day_low_tide_date = tab[1].split('(')[1][4:].replace(
                    ')', '') + ' ' + str(datetime.today().year)
                result['Low Tide Time'] = self.verify_between_sunrise_and_sunset(
                    result, day_low_tide_time)
                result['Low Tide Height'] = tab[2]
                if 'Day' not in result:
                    result['Day'] = day_low_tide_date

    def verify_between_sunrise_and_sunset(self, result, day_low_tide_time):
        sunrise_datetime = datetime.strptime(
            result['Sunrise'], '%I:%M%p')
        sunset_datetime = datetime.strptime(
            result['Sunset'], '%I:%M%p')
        if day_low_tide_time.startswith('00'):
            day_low_tide_time = day_low_tide_time.replace('00', '12')
        low_tide_datetime = datetime.strptime(
            day_low_tide_time, '%I:%M %p')

        if low_tide_datetime > sunrise_datetime and low_tide_datetime < sunset_datetime:
            return day_low_tide_time


ScrapeTideForecast = ScrapeTideForecast()

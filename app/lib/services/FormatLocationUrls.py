class FormatLocationUrls:

    def hyphenate_locations(self, locations):
        base_url = 'https://www.tide-forecast.com/locations/?/tides/latest'

        hyphenated_locations = []

        for loc in locations:
            url_loc = loc.replace(',', '').replace(' ', '-')
            final_url = base_url.replace('?', url_loc)
            hyphenated_locations.append(final_url)

        return hyphenated_locations


FormatLocationUrls = FormatLocationUrls()

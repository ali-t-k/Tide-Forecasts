from app.data.TideLocations import TideLocations
from app.lib.services.FormatLocationUrls import FormatLocationUrls
from app.lib.services.OutputFile import OutputFile
from app.lib.services.ScrapeTideForecast import ScrapeTideForecast


if __name__ == '__main__':
    tide_locations = TideLocations.tide_locations()
    formatted_location_urls = FormatLocationUrls.hyphenate_locations(
        tide_locations)
    tide_forecasts = ScrapeTideForecast.scrape_tide_forecast(
        formatted_location_urls)
    OutputFile.write_output(tide_forecasts)

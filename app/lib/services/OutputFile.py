import json


class OutputFile:
    def write_output(self, tide_forecasts):
        with open('output_file.txt', 'w') as f_out:
            json.dump(tide_forecasts, f_out, indent=4, sort_keys=True)


OutputFile = OutputFile()

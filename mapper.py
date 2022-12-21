import json
import datetime
import sys
from itertools import groupby


class Mapper:
    csv_data, temp_data, res_data = [], [], []

    def parse(self, lines_from_file):
        for index, line in enumerate(lines_from_file):
            if index != 0:
                local_dict = {
                    "location": line.split(";")[2],
                    "date": line.split(";")[3],
                    "total_cases": line.split(";")[4]
                }
                self.csv_data.append(local_dict)

    def get_data(self):
        locations, dates, total_cases = [], [], []
        for element in self.csv_data:
            locations.append(element["location"])
            dates.append(element["date"])
            total_cases.append(element["total_cases"])

        self.temp_data = list(zip(locations, dates, total_cases))
        keyfunc = lambda x: x[0]

        for location, action in groupby(self.temp_data, key=keyfunc):
            model = {}
            init_values, res_values = [], []

            for _, date, total in action:
                values_model = {"date": date, "total_cases": total}
                init_values.append(values_model)

            last_date = datetime.datetime.strptime(init_values[-1]["date"], "%Y-%m-%d")
            first_fate = datetime.datetime.strptime(init_values[0]["date"], "%Y-%m-%d")
            days_count = (last_date - first_fate).days

            last_total = int(init_values[-1]["total_cases"])
            first_total = int(init_values[0]["total_cases"])
            total_diff = last_total - first_total

            if len(init_values) > 1:
                model["location"] = location
                model["values"] = {"days_count": days_count, "total_diff": total_diff}

                self.res_data.append(model)

    def show(self):
        for element in self.res_data:
            print(element)

    def save_to_json(self, output_file_path):
        with open(output_file_path, "w") as file:
            json.dump(self.res_data, file)


def start():
    mapper = Mapper()
    mapper.parse(lines_from_file=sys.stdin)
    mapper.get_data()
    mapper.show()


if __name__ == "__main__":
    start()

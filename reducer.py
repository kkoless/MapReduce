import json
import sys
import time


class Reducer:
    json_data, res_data = [], []

    def parse(self, line_from_lines):
        for line in line_from_lines:
            new_line = line.split("\n")[0].replace("'", "\"")
            self.json_data.append(json.loads(new_line))

    def work(self):
        for element in self.json_data:
            local_array = {"location": element["location"],
                           "result": (element["values"]["total_diff"] / element["values"]["days_count"])}
            self.res_data.append(local_array)

    def show(self):
        for element in self.res_data:
            print(element)

    def save_to_json(self, output_file_path):
        with open(output_file_path, "w") as file:
            json.dump(self.res_data, file)


def start():
    time.sleep(1)
    reducer = Reducer()
    reducer.parse(line_from_lines=sys.stdin)
    reducer.work()
    reducer.show()


if __name__ == "__main__":
    start()

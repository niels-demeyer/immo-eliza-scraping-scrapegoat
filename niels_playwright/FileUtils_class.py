import os
import shutil
import json
import csv


class FileUtils:
    @staticmethod
    def write_json_file(file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def read_json_file(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    def check_duplicates_json_file(file_path, data):
        with open(file_path, "r") as f:
            old_data = json.load(f)
            for d in data:
                if d not in old_data:
                    old_data.append(d)
        with open(file_path, "w") as f:
            json.dump(old_data, f, indent=4)

    def return_solo_items(data):
        solo_items = []
        for item in data:
            if "href" in item:
                if item["href"] not in solo_items:
                    solo_items.append(item["href"])
        return solo_items

    @staticmethod
    def write_dict_to_csv(file_path, data):
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def remove_directory(directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)

    @staticmethod
    def copy_file(src, dst):
        shutil.copyfile(src, dst)

    @staticmethod
    def move_file(src, dst):
        shutil.move(src, dst)

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def list_files(directory):
        return os.listdir(directory)

    @staticmethod
    def list_files_with_extension(directory, extension):
        return [f for f in os.listdir(directory) if f.endswith(extension)]

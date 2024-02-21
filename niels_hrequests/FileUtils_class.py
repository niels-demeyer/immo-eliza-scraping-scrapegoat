import os
import shutil
import json
import csv


class FileUtils:
    @staticmethod
    def flatten_dict(d, parent_key="", sep="_"):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(FileUtils.flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, elem in enumerate(v):
                    if isinstance(elem, dict):
                        items.extend(
                            FileUtils.flatten_dict(
                                elem, f"{new_key}{sep}{i}", sep=sep
                            ).items()
                        )
                    else:
                        items.append((f"{new_key}{sep}{i}", elem))
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def write_dict_to_csv(file_path, data):
        # Check if data is a list
        if isinstance(data, list):
            # Flatten each dictionary in the list
            flat_data_list = [FileUtils.flatten_dict(item) for item in data]
        else:
            # If data is not a list, assume it's a dictionary and flatten it
            flat_data_list = [FileUtils.flatten_dict(data)]

        # Get all keys used in any dictionary
        all_keys = set().union(*(d.keys() for d in flat_data_list))

        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            for flat_data in flat_data_list:
                writer.writerow(flat_data)

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

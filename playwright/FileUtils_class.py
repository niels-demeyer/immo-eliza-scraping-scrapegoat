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
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(
                            FileUtils.flatten_dict(
                                item, f"{new_key}_{i}", sep=sep
                            ).items()
                        )
                    else:
                        items.append((f"{new_key}_{i}", item))
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def write_dict_to_csv(file_path, data):
        flat_data = [FileUtils.flatten_dict(row) for row in data]
        all_keys = set().union(*[row.keys() for row in flat_data])
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            for row in flat_data:
                # Fill in missing keys with 0, replace newline characters and commas in string values
                row_with_defaults = {
                    key: (
                        str(row.get(key, 0)).replace("\n", " ").replace(",", ";")
                        if isinstance(row.get(key, 0), str)
                        else row.get(key, 0)
                    )
                    for key in all_keys
                }
                writer.writerow(row_with_defaults)

    @staticmethod
    def write_json_file(file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def read_json_file(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def check_duplicates_json_file(file_path, data):
        with open(file_path, "r") as f:
            old_data = json.load(f)
            for d in data:
                if d not in old_data:
                    old_data.append(d)
        with open(file_path, "w") as f:
            json.dump(old_data, f, indent=4)

    @staticmethod
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

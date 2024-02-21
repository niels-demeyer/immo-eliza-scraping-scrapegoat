import os
import json


def read_json_file(file_path, encoding="ISO-8859-1"):
    with open(file_path, "r", encoding=encoding) as f:
        return json.load(f)


def format_clean_urls():
    # Load the data from the file
    data = read_json_file("clean_urls.json", encoding="ISO-8859-1")
    return data


def unpack_data(data):
    data_list = [{"immo_id": k, "href": v} for k, v in data.items()]
    return data_list


def save_json_file(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


data = format_clean_urls()


data_dict = unpack_data(data=data)
print(type(data_dict))
print(len(data_dict))
print(data_dict[0])

save_json_file("format_clean_urls.json", data_dict)
print("File saved.")

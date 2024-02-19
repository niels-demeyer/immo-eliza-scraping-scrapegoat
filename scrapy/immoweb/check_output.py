import json

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def check_duplicates(data):
    seen = {}
    duplicates = []
    for item in data:
        # Assuming each item is a dict and 'href' is the unique identifier
        href = item['href']
        if href in seen:
            duplicates.append(item)
        else:
            seen[href] = item
    return duplicates

# Read data from file
data = read_json_file('./immoweb/output.json')

# Check for duplicates
duplicates = check_duplicates(data)

# Print the number of duplicates
print(len(duplicates))

# Print the duplicates
for duplicate in duplicates:
    print(duplicate)
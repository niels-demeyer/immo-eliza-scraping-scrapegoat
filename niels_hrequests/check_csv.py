import pandas as pd
from pprint import pprint

# Load the CSV file as a pandas DataFrame with 'latin1' encoding
df = pd.read_csv("result.csv", encoding="latin1")

# Now df is a DataFrame, and you can use pandas methods on it.
# Set the options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

# Now when you display a DataFrame, it will show all rows and columns
print(df.columns)
print(df.columns[0:100])
print(df.columns[100:200])
print(df.columns[200:300])
print(df.columns[300:-1])

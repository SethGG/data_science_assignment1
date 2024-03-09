# The code in this file is responsible for:
# - Finding all CSV files in the path
# - Loading all CSV files into DataFrames
# - Preprocessing the DataFrames
# - Concatenating the DataFrames per month into a single DataFrame for sales, crashes and ratings

import pandas as pd
import glob

# List the path names for all CSV files
path = "assignment1 data"
sales_files = glob.glob(path + "/sales_*.csv")
crashes_files = glob.glob(path + "/stats_crashes_*_overview.csv")
ratings_country_files = glob.glob(path + "/stats_ratings_*_country.csv")
ratings_overview_files = glob.glob(path + "/stats_ratings_*_overview.csv")


def preprocessing(dfs, column_renames, row_conditions, select_columns, date_column):
    """
    Helper function for preprocessing the datasets.
    Parameters:
        dfs: list of DataFrames to be processed
        column_renames: dict with columns to be renamed (key to value)
        row_conditions: dict with conditions on which rows should be selected (key is column and value is target value)
        select_columns: list of columns to include in the output
        data_column: the name of the column containing date information (used to sort)
    Returns: A concatenated DataFrame from all the processed DataFrames ordered by date
    """
    processed_dfs = []
    for df in dfs:
        # Rename columns as defined in column_renames
        df = df.rename(columns={k: v for k, v in column_renames.items() if k in df.columns})
        # Select rows based on conditions in row_conditions
        for k, v in row_conditions.items():
            if k in df.columns:
                df = df[df[k] == v]
        # Select columns as difined in select_columns
        df = df[select_columns]
        processed_dfs.append(df)
    # Combine the processed DataFrames into a single DataFrame
    combined_df = pd.concat(processed_dfs)
    return combined_df.sort_values(date_column).reset_index(drop=True)


#######################
# Sales Preprocessing #
#######################

# Read each CSV file into a DataFrame
divergent_files = ("sales_202111.csv", "sales_202112.csv")
sales_dfs = []
for file in sales_files:
    df = pd.read_csv(file, thousands=",")
    if file.endswith(divergent_files):
        df["Datetime"] = pd.to_datetime(df["Order Charged Timestamp"], unit="s")
        df["Datetime"] = df["Datetime"].dt.tz_localize("UTC")
    else:
        df["Transaction Time"] = df["Transaction Time"].str.replace("PDT", "")
        df["Datetime"] = pd.to_datetime(df["Transaction Date"] + " " + df["Transaction Time"])
        df["Datetime"] = df["Datetime"].dt.tz_localize("America/Los_Angeles").dt.tz_convert("UTC")
    sales_dfs.append(df)

# Columns to be renamed in the DataFrames (old name, new name)
column_renames = {
    'Product ID': 'Product id',
    'SKU ID': 'Sku Id',
    'Country of Buyer': 'Buyer Country',
    'Postal Code of Buyer': 'Buyer Postal Code',
    'Charged Amount': 'Amount (Merchant Currency)'
}
# Conditions to select rows on in the DataFrames
row_conditions = {
    'Transaction Type': 'Charge',
    'Product id': 'com.vansteinengroentjes.apps.ddfive'
}
# Columns to select in the DataFrames
select_columns = [
    'Datetime',
    'Sku Id',
    'Buyer Country',
    'Buyer Postal Code',
    'Amount (Merchant Currency)'
]
# The name of the date column that has to be converted
date_column = 'Datetime'

# The final processed DataFrame to be used by the dashboard
sales = preprocessing(sales_dfs, column_renames, row_conditions, select_columns, date_column)

#########################
# Crashes Preprocessing #
#########################

# Read each CSV file into a DataFrame
crashes_dfs = [pd.read_csv(file, encoding='utf-16', parse_dates=["Date"]) for file in crashes_files]

# Columns to select in the DataFrames
select_columns = [
    'Date',
    'Daily Crashes',
    'Daily ANRs'
]
# The name of the date column that has to be converted
date_column = 'Date'

# The final processed DataFrame to be used by the dashboard
crashes = preprocessing(crashes_dfs, {}, {}, select_columns, date_column)

#########################
# Ratings Preprocessing #
#########################

# Read each CSV file into a DataFrame
ratings_country_dfs = [pd.read_csv(file, encoding='utf-16', parse_dates=["Date"]) for file in ratings_country_files]

# Columns to select in the DataFrames
select_columns = [
    'Date',
    'Country',
    'Daily Average Rating',
    'Total Average Rating'
]
# The name of the date column that has to be converted
date_column = 'Date'

# The final processed DataFrame to be used by the dashboard
ratings_country = preprocessing(ratings_country_dfs, {}, {}, select_columns, date_column)

#########################################################################################

# Read each CSV file into a DataFrame
ratings_overview_dfs = [pd.read_csv(file, encoding='utf-16', parse_dates=["Date"]) for file in ratings_overview_files]

# Columns to select in the DataFrames
select_columns = [
    'Date',
    'Daily Average Rating',
    'Total Average Rating'
]
# The name of the date column that has to be converted
date_column = 'Date'

# The final processed DataFrame to be used by the dashboard
ratings_overview = preprocessing(ratings_overview_dfs, {}, {}, select_columns, date_column)

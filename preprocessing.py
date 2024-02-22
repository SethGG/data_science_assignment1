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
ratings_files = glob.glob(path + "/stats_ratings_*_country.csv")


def preprocessing(dfs, column_renames, row_conditions, select_columns, date_column):
    """
    Helper function for preprocessing the datasets.
    Parameters:
        dfs: list of DataFrames to be processed
        column_renames: dict with columns to be renamed (key to value)
        row_conditions: dict with conditions on which rows should be selected (key is column and value is target value)
        select_columns: list of columns to include in the output
        data_column: the name of the column containing date information
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
        # Convert the date_column to the date time object
        df[date_column] = pd.to_datetime(df[date_column])
        processed_dfs.append(df)
    # Combine the processed DataFrames into a single DataFrame
    return pd.concat(processed_dfs, ignore_index=True).sort_values([date_column])


#######################
# Sales Preprocessing #
#######################

# Read each CSV file into a DataFrame
sales_dfs = [pd.read_csv(file) for file in sales_files]
# Columns to be renamed in the DataFrames (old name, new name)
column_renames = {
    'Order Charged Date': 'Transaction Date',
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
    'Transaction Date',
    'Sku Id',
    'Buyer Country',
    'Buyer Postal Code'
]
# The name og the date column that has to be converted
date_column = 'Transaction Date'

# The final processed DataFrame to be used by the dashboard
sales = preprocessing(sales_dfs, column_renames, row_conditions, select_columns, date_column)

#########################
# Crashes Preprocessing #
#########################

# Read each CSV file into a DataFrame
crashes_dfs = [pd.read_csv(file, encoding='utf-16') for file in crashes_files]
# Columns to select in the DataFrames
select_columns = [
    'Date',
    'Daily Crashes',
    'Daily ANRs'
]
# The name og the date column that has to be converted
date_column = 'Date'

# The final processed DataFrame to be used by the dashboard
crashes = preprocessing(crashes_dfs, {}, {}, select_columns, date_column)

#########################
# Ratings Preprocessing #
#########################

# Read each CSV file into a DataFrame
ratings_dfs = [pd.read_csv(file, encoding='utf-16') for file in ratings_files]
# Columns to select in the DataFrames
select_columns = [
    'Date',
    'Country',
    'Daily Average Rating',
    'Total Average Rating'
]
# The name og the date column that has to be converted
date_column = 'Date'

# The final processed DataFrame to be used by the dashboard
ratings = preprocessing(ratings_dfs, {}, {}, select_columns, date_column)

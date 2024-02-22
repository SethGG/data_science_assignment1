import pandas as pd
import glob

# List the path names for all CSV files
path = "assignment1 data"
sales_files = glob.glob(path + "/sales_*.csv")
crashes_files = glob.glob(path + "/stats_crashes_*_overview.csv")
ratings_files = glob.glob(path + "/stats_rating_*_country.csv")

#######################
# Sales Proprocessing #
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
    'Transaction Type': 'Charge'
}
# Columns to select in the DataFrames
select_columns = [
    'Transaction Date',
    'Product id',
    'Sku Id',
    'Buyer Country',
    'Buyer Postal Code'
]
# The name og the date column that has to be converted
date_column = 'Transaction Date'

processed_sales_dfs = []
for df in sales_dfs:
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
    processed_sales_dfs.append(df)

# Combine the processed DataFrames into a single DataFrame
sales = pd.concat(processed_sales_dfs, ignore_index=True)

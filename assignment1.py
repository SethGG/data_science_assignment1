import pandas as pd
import glob

# List the path names for all CSV files
path = "assignment1 data"
sales_files = glob.glob(path + "/sales_*.csv")
crashes_files = glob.glob(path + "/stats_crashes_*_overview.csv")
ratings_files = glob.glob(path + "/stats_rating_*_country.csv")

# Read each CSV file into a DataFrame
sales_dfs = [pd.read_csv(file) for file in sales_files]
column_renames = {
    'Order Charged Date': 'Transaction Date',
    'Product ID': 'Product id',
    'SKU ID': 'Sku Id',
    'Country of Buyer': 'Buyer Country',
    'Postal Code of Buyer': 'Buyer Postal Code',
    'Charged Amount': 'Amount (Merchant Currency)'
}
row_conditions = {
    'Transaction Type': 'Charge'
}

for df in sales_dfs:
    df.rename(columns={k: v for k, v in column_renames.items() if k in df.columns}, inplace=True)
    for k, v in row_conditions.items():
        if k in df.columns:
            df = df[df[k] == v]


# for df in sales_dfs:
#    print(df.columns)
# crashes = pd.concat((pd.read_csv(file) for file in crashes_files))
# ratings = pd.concat((pd.read_csv(file) for file in ratings_files))

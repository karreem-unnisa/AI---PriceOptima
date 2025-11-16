import pandas as pd
df_inventory = pd.read_csv('retail_store_inventory.csv')
df_marketplace = pd.read_csv('popular_ecomm_marketplace-Ecommerce__20231101_20231130_sample (2).csv')
df_pricing = pd.read_csv('dynamic_pricing.csv')
print(df_inventory.head())
print(df_marketplace.head())
print(df_pricing.head())

print("Inventory:", df_inventory.shape)
print("Marketplace:", df_marketplace.shape)
print("Pricing:", df_pricing.shape)

print("Inventory columns:", df_inventory.columns.tolist())
print("Marketplace columns:", df_marketplace.columns.tolist())
print("Pricing columns:", df_pricing.columns.tolist())

print(df_inventory.info())
print(df_marketplace.info())
print(df_pricing.info())

print(df_inventory.isnull().sum())
print(df_marketplace.isnull().sum())
print(df_pricing.isnull().sum())

if 'inventory_available' in df_inventory.columns:
    df_inventory['inventory_available'].fillna(0, inplace=True)

df_marketplace.ffill(inplace=True) 
pricing_drop_cols = [col for col in ['price', 'units_sold'] if col in df_pricing.columns]
if pricing_drop_cols:
    df_pricing.dropna(subset=pricing_drop_cols, inplace=True)
else:
    df_pricing.dropna(inplace=True)

df_inventory.drop_duplicates(inplace=True)
df_marketplace.drop_duplicates(inplace=True)
df_pricing.drop_duplicates(inplace=True)

for df in [df_inventory, df_marketplace, df_pricing]:
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

for df in [df_inventory, df_marketplace, df_pricing]:
    for col in ['price', 'units_sold', 'inventory_available', 'competitor_price']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
for dfx in [df_marketplace, df_pricing]:
    if 'price' in dfx.columns:
        dfx = dfx[dfx['price'] < dfx['price'].quantile(0.99)]
    if 'units_sold' in dfx.columns:
        dfx = dfx[dfx['units_sold'] < dfx['units_sold'].quantile(0.99)]
merge_keys = [key for key in ['product_id', 'date']
              if key in df_pricing.columns and key in df_inventory.columns and key in df_marketplace.columns]
if merge_keys:
    merged = pd.merge(df_pricing, df_inventory, on=merge_keys, how='left')
    merged = pd.merge(merged, df_marketplace, on=merge_keys, how='left')
else:
    merged = df_pricing.copy()

merged.to_csv('priceoptima_cleaned.csv', index=False)
print("Cleaned dataset saved as priceoptima_cleaned.csv")

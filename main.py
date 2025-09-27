import pandas as pd
import glob
import matplotlib.pyplot as plt

# Step 1: Collect all CSV files
csv_files = glob.glob("data/*.csv")

all_data = []

for file in csv_files:
    df = pd.read_csv(file)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Normalize product names (lowercase, strip spaces)
    df["product"] = df["product"].str.strip().str.lower()

    # Clean price column (remove $ and convert to float)
    df["price"] = df["price"].replace(r'[\$,]', '', regex=True).astype(float)

    # Filter only pink morsel
    df = df[df["product"] == "pink morsel"]

    # Compute sales
    df["sales"] = df["quantity"] * df["price"]

    # Keep only required fields
    df = df[["sales", "date", "region"]]

    all_data.append(df)

# Merge
final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv("final_sales.csv", index=False)
print("✅ Final CSV created with", len(final_df), "rows")

# ---------------- Visualization ---------------- #
region_filter = input("Enter region to filter (or press Enter for all): ").strip()

if region_filter:
    filtered_df = final_df[final_df["region"].str.lower() == region_filter.lower()]
    if filtered_df.empty:
        print(f"No data for region '{region_filter}'. Showing all instead.")
        filtered_df = final_df
else:
    filtered_df = final_df

# Convert date to datetime
filtered_df["date"] = pd.to_datetime(filtered_df["date"])

# Plot: Sales over time
plt.figure(figsize=(8,5))
plt.plot(filtered_df["date"], filtered_df["sales"], marker="o")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.title(f"Sales Over Time {'('+region_filter+')' if region_filter else ''}")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot: Total sales by region
region_sales = final_df.groupby("region")["sales"].sum().reset_index()
plt.figure(figsize=(6,4))
plt.bar(region_sales["region"], region_sales["sales"])
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.title("Total Sales by Region")
plt.show()

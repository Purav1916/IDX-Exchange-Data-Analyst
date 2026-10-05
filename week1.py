import pandas as pd
import glob
import os

# Get the folder where this Python script is located
script_folder = os.path.dirname(os.path.abspath(__file__))

# CSV folder is one folder above the py folder
csv_folder = os.path.join(script_folder, "..", "CSV")

# Find all monthly listing and sold CSV files
listing_files = sorted(
    glob.glob(os.path.join(csv_folder, "CRMLSListing*.csv"))
)

sold_files = sorted(
    glob.glob(os.path.join(csv_folder, "CRMLSSold*.csv"))
)

print("Listing files found:", len(listing_files))
print("Sold files found:", len(sold_files))


# -------------------------
# LISTING DATA
# -------------------------

listing_dataframes = []

for file in listing_files:
    df = pd.read_csv(file, low_memory=False)
    listing_dataframes.append(df)

# Row count before concatenation:
# 860,898 total rows across the 28 individual listing files
listing_rows_before_concat = sum(len(df) for df in listing_dataframes)

# Combine all monthly listing files
listings = pd.concat(listing_dataframes, ignore_index=True)

# Row count after concatenation:
# 860,898 rows
listing_rows_after_concat = len(listings)


# -------------------------
# SOLD DATA
# -------------------------

sold_dataframes = []

for file in sold_files:
    df = pd.read_csv(file, low_memory=False)
    sold_dataframes.append(df)

# Row count before concatenation:
# 615,707 total rows across the 28 individual sold files
sold_rows_before_concat = sum(len(df) for df in sold_dataframes)

# Combine all monthly sold files
sold = pd.concat(sold_dataframes, ignore_index=True)

# Row count after concatenation:
# 615,707 rows
sold_rows_after_concat = len(sold)


# Display concatenation row counts
print("\nConcatenation:")
print("Listing rows before concatenation:", listing_rows_before_concat)
print("Listing rows after concatenation:", listing_rows_after_concat)
print("Sold rows before concatenation:", sold_rows_before_concat)
print("Sold rows after concatenation:", sold_rows_after_concat)


# -------------------------
# RESIDENTIAL FILTER
# -------------------------

# Row counts before Residential filter:
# Listings: 860,898
# Sold: 615,707
listing_rows_before_filter = len(listings)
sold_rows_before_filter = len(sold)

# Keep only Residential properties
listings = listings[listings["PropertyType"] == "Residential"]
sold = sold[sold["PropertyType"] == "Residential"]

# Row counts after Residential filter:
# Listings: 547,162
# Sold: 414,054
listing_rows_after_filter = len(listings)
sold_rows_after_filter = len(sold)

print("\nResidential Filter:")
print("Listings before filter:", listing_rows_before_filter)
print("Listings after filter:", listing_rows_after_filter)
print("Sold before filter:", sold_rows_before_filter)
print("Sold after filter:", sold_rows_after_filter)


# -------------------------
# SAVE RESULTS
# -------------------------

listings_output = os.path.join(
    csv_folder,
    "Combined_Residential_Listings.csv"
)

sold_output = os.path.join(
    csv_folder,
    "Combined_Residential_Sold.csv"
)

listings.to_csv(listings_output, index=False)
sold.to_csv(sold_output, index=False)

print("\nFiles saved successfully:")
print("Combined_Residential_Listings.csv")
print("Combined_Residential_Sold.csv")
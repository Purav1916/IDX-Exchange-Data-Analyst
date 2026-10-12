import pandas as pd
from pathlib import Path

#lovate the CSV folder
csv_folder = Path(__file__).resolve().parent.parent / "CSV"

#Load week1 datasets
listings = pd.read_csv(
    csv_folder / "Combined_Residential_Listings.csv",
    low_memory=False
)


sold = pd.read_csv(
    csv_folder / "Combined_Residential_Sold.csv",
    low_memory=False
)

print("Listings:", listings.shape)
print("Sold:", sold.shape)


#Inspect dataset structure
print("\n----Listings Columns----")
print(listings.columns.tolist())

print("\n----Sold Columns----")
print(sold.columns.tolist())

#Check data types
print("\n----Listings Data Types----")
print(listings.dtypes)

print("\n----Sold Data Types----")
print(sold.dtypes)

#Check unique property types
print("\n----Unique Property Types in Types----")
print("ListingsL", listings["PropertyType"].unique()) #selects the PropertyType column from the Listings dataset
print("Sold:", sold["PropertyType"].unique()) #selects the PropertyType column from the Sold dataset


#Missing value analysis 
print("\n----Missing Values in Listings----")
print(listings.isnull().sum().to_string()) #checks which values are missing and counts how many they are

print("\n----Missing Values in Sold----")
print(sold.isnull().sum().to_string()) #checks which values are missing and counts how many they are


# Calulate missing percentage
listings_missing_percentage = listings.isnull().mean() * 100
sold_missing_percentage = sold.isnull().mean() * 100

print("\n----Missing Percentage in Listings with more than 90%----")
print(listings_missing_percentage[listings_missing_percentage > 90])

print("\n----Missing Percentage in Sold with more than 90%----")
print(sold_missing_percentage[sold_missing_percentage > 90])


#separate market analysis fields from metadata fields
market_fields = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "DaysOnMarket",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "YearBuilt",
    "PropertyType",
    "PropertySubType",
    "CountyOrParish",
    "City",
    "PostalCode"
]


metadata_fields = [
    "ListingKey",
    "ListingId",
    "ListingKeyNumeric",
    "ListAgentEmail",
    "ListAgentFirstName",
    "ListAgentLastName"
]


print("\n----Market Analysis Fields----")
print(sold[market_fields].head()) #selects only market_fields columns and displays first 5


print("\n----Metadata Analysis Fields----")
print(sold[metadata_fields].head()) #selects only metadata_fields columns and displays first 5


# Create missing value summary tables
listings_summary = pd.DataFrame({
    "Missing Count": listings.isnull().sum(),
    "Missing Percentage": listings.isnull().mean() * 100
})

sold_summary = pd.DataFrame({
    "Missing Count": sold.isnull().sum(),
    "Missing Percentage": sold.isnull().mean() * 100
})

# Sort by highest missing percentage
listings_summary = listings_summary.sort_values(
    by="Missing Percentage", ascending=False
)

sold_summary = sold_summary.sort_values(
    by="Missing Percentage", ascending=False
)

print("\n----Listings Missing Summary----")
print(listings_summary.to_string())

print("\n----Sold Missing Summary----")
print(sold_summary.to_string())



core_fields = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "DaysOnMarket",
    "PropertyType",
    "PropertySubType",
    "CountyOrParish",
    "City",
    "PostalCode",
    "CloseDate",
    "ListingContractDate"
]

#identify columns with more than 90% missing values
listings_drop_candidates = listings_missing_percentage[
    (listings_missing_percentage > 90) & #checks which columns has more than 90% missing values
    (~listings_missing_percentage.index.isin(core_fields)) #checks if the column is part of core fields
]

sold_drop_candidates = sold_missing_percentage[
    (sold_missing_percentage > 90) & #checks which columns has more than 90% missing values
    (~sold_missing_percentage.index.isin(core_fields)) #checks if the column is part of core fields
]


print("\n----Listings Drop Candidates----")
print(listings_drop_candidates)

print("\n----Sold Drop Candidates----")
print(sold_drop_candidates)

print("\nCore fields will be retained for future analysis.")


listings_summary.to_csv(
    csv_folder / "Week2_Listings_Missing_Summary.csv"
)

sold_summary.to_csv(
    csv_folder / "Week2_Sold_Missing_Summary.csv"
)

print("\nWeek 2 missing-value reports saved successfully.")
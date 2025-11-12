"""
EPA Smart Location Database - Data Cleaning and Normalization Script
This script cleans and normalizes the EPA Smart Location Database V3 dataset.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("Loading EPA Smart Location Database...")
df = pd.read_csv('EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv')

print(f"\nInitial dataset shape: {df.shape}")
print(f"Total rows: {df.shape[0]:,}")
print(f"Total columns: {df.shape[1]}")

# ============================================================================
# DATA QUALITY ASSESSMENT
# ============================================================================
print("\n" + "="*80)
print("DATA QUALITY ASSESSMENT")
print("="*80)

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"\n1. Duplicate rows: {duplicates}")

# Check for missing values
print("\n2. Missing values by column:")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing_Count': missing,
    'Missing_Percentage': missing_pct
}).sort_values('Missing_Count', ascending=False)

# Display only columns with missing values
missing_with_nulls = missing_df[missing_df['Missing_Count'] > 0]
if len(missing_with_nulls) > 0:
    print(missing_with_nulls.head(20))
else:
    print("No missing values found!")

# Check data types
print("\n3. Data types summary:")
print(df.dtypes.value_counts())

# Check for potential issues with numeric columns stored as objects
print("\n4. Checking for numeric columns stored as text...")
object_cols = df.select_dtypes(include=['object']).columns
problematic_cols = []
for col in object_cols:
    # Skip obvious text columns
    if col in ['GEOID10', 'GEOID20', 'CSA_Name', 'CBSA_Name', 'STATEFP', 'COUNTYFP', 'TRACTCE', 'BLKGRPCE']:
        continue
    try:
        # Try to convert to numeric
        pd.to_numeric(df[col], errors='raise')
        problematic_cols.append(col)
    except:
        pass

if problematic_cols:
    print(f"Found {len(problematic_cols)} numeric columns stored as text:")
    for col in problematic_cols[:10]:
        print(f"  - {col}")
else:
    print("No obvious issues found.")

# ============================================================================
# DATA CLEANING
# ============================================================================
print("\n" + "="*80)
print("DATA CLEANING")
print("="*80)

df_clean = df.copy()

# 1. Remove exact duplicates
print("\n1. Removing duplicate rows...")
initial_rows = len(df_clean)
df_clean = df_clean.drop_duplicates()
removed_duplicates = initial_rows - len(df_clean)
print(f"   Removed {removed_duplicates} duplicate rows")

# 2. Handle missing values
print("\n2. Handling missing values...")

# Define columns to handle differently
geographic_identifiers = ['CSA', 'CBSA', 'CSA_Name', 'CBSA_Name']
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns

for col in numeric_cols:
    missing_count = df_clean[col].isnull().sum()
    if missing_count > 0:
        missing_pct = (missing_count / len(df_clean)) * 100
        
        # Skip CSA and CBSA - these should remain missing
        if col in geographic_identifiers:
            print(f"   {col}: {missing_count} missing values ({missing_pct:.2f}%) - KEPT AS MISSING (not in metro area)")
            continue
        
        # If more than 50% missing, flag as warning
        if missing_pct > 50:
            print(f"   WARNING: {col} has {missing_pct:.2f}% missing values")
        
        # Fill with 0 for counts/employment data, median for other metrics
        if any(x in col.upper() for x in ['EMP', 'POP', 'WORKERS', 'COUNT', 'HH', 'TOT']):
            df_clean[col].fillna(0, inplace=True)
            print(f"   Filled {col} missing values with 0 ({missing_count} values)")
        else:
            median_val = df_clean[col].median()
            df_clean[col].fillna(median_val, inplace=True)
            print(f"   Filled {col} missing values with median: {median_val:.4f} ({missing_count} values)")

# Create binary indicators for CSA and CBSA membership
print("\n2b. Creating metro area indicators...")
df_clean['In_CSA'] = df_clean['CSA'].notna().astype(int)
df_clean['In_CBSA'] = df_clean['CBSA'].notna().astype(int)
print(f"   Created In_CSA: {df_clean['In_CSA'].sum():,} block groups in Combined Statistical Areas")
print(f"   Created In_CBSA: {df_clean['In_CBSA'].sum():,} block groups in Core Based Statistical Areas")

# 3. Fix data types - convert GEOID columns to strings to preserve leading zeros
print("\n3. Fixing data types...")
geoid_cols = ['GEOID10', 'GEOID20', 'STATEFP', 'COUNTYFP', 'TRACTCE', 'BLKGRPCE']
for col in geoid_cols:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].astype(str)
        # Ensure proper formatting (e.g., state codes should be 2 digits)
        if col == 'STATEFP':
            df_clean[col] = df_clean[col].str.zfill(2)
        print(f"   Converted {col} to string type")

# Convert CSA and CBSA to strings (categorical codes)
if 'CSA' in df_clean.columns:
    df_clean['CSA'] = df_clean['CSA'].astype(str).replace('nan', np.nan)
    print(f"   Converted CSA to string type (categorical)")
if 'CBSA' in df_clean.columns:
    df_clean['CBSA'] = df_clean['CBSA'].astype(str).replace('nan', np.nan)
    print(f"   Converted CBSA to string type (categorical)")

# 4. Remove rows with invalid core identifiers
print("\n4. Checking for invalid core identifiers...")
initial_rows = len(df_clean)
# Keep only rows where GEOID10 is valid (not null, not empty)
df_clean = df_clean[df_clean['GEOID10'].notna()]
df_clean = df_clean[df_clean['GEOID10'] != '']
df_clean = df_clean[df_clean['GEOID10'] != 'nan']
removed_invalid = initial_rows - len(df_clean)
if removed_invalid > 0:
    print(f"   Removed {removed_invalid} rows with invalid identifiers")
else:
    print("   No invalid identifiers found")

# 5. Handle outliers in key numeric columns
print("\n5. Detecting outliers in key numeric columns...")
outlier_cols = ['TotPop', 'TotEmp', 'Workers', 'Ac_Land', 'Ac_Total']
for col in outlier_cols:
    if col in df_clean.columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR  # Using 3*IQR for less aggressive filtering
        upper_bound = Q3 + 3 * IQR
        outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
        outlier_pct = (outliers / len(df_clean)) * 100
        print(f"   {col}: {outliers} potential outliers detected ({outlier_pct:.2f}%) - NOT REMOVED (may be real extreme values)")

# ============================================================================
# DATA NORMALIZATION
# ============================================================================
print("\n" + "="*80)
print("DATA NORMALIZATION")
print("="*80)

df_normalized = df_clean.copy()

# 1. Create normalized versions of key metrics (0-1 scale)
print("\n1. Creating normalized versions of key metrics...")
metrics_to_normalize = [
    'TotPop', 'TotEmp', 'Workers', 'D1A', 'D1B', 'D1C', 
    'D2A_JPHH', 'D3B', 'D4A', 'D5AR', 'D5AE'
]

for col in metrics_to_normalize:
    if col in df_normalized.columns:
        col_min = df_normalized[col].min()
        col_max = df_normalized[col].max()
        if col_max - col_min > 0:  # Avoid division by zero
            df_normalized[f'{col}_normalized'] = (df_normalized[col] - col_min) / (col_max - col_min)
            print(f"   Created {col}_normalized")

# 2. Standardize percentage columns (ensure they're between 0 and 1)
print("\n2. Standardizing percentage columns...")
pct_cols = [col for col in df_normalized.columns if 'Pct' in col or 'PCT' in col or col.startswith('P_')]
for col in pct_cols:
    if df_normalized[col].max() > 1:
        # Convert from 0-100 to 0-1 scale
        df_normalized[col] = df_normalized[col] / 100
        print(f"   Standardized {col} to 0-1 scale")

# 3. Create density categories
print("\n3. Creating categorical variables from continuous metrics...")
if 'D1A' in df_normalized.columns:
    df_normalized['PopDensity_Category'] = pd.cut(
        df_normalized['D1A'],
        bins=[0, 1, 5, 10, 20, float('inf')],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
    )
    print("   Created PopDensity_Category")

if 'D1B' in df_normalized.columns:
    df_normalized['EmpDensity_Category'] = pd.cut(
        df_normalized['D1B'],
        bins=[0, 1, 5, 10, 20, float('inf')],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
    )
    print("   Created EmpDensity_Category")

if 'NatWalkInd' in df_normalized.columns:
    df_normalized['Walkability_Category'] = pd.cut(
        df_normalized['NatWalkInd'],
        bins=[0, 5, 10, 15, 20],
        labels=['Low', 'Medium', 'High', 'Very High'],
        include_lowest=True
    )
    print("   Created Walkability_Category")

# Create urban/rural classification based on metro area membership
print("\n3b. Creating urban/rural classification...")
df_normalized['Urban_Rural'] = 'Rural'
df_normalized.loc[df_normalized['In_CBSA'] == 1, 'Urban_Rural'] = 'Urban'
urban_count = (df_normalized['Urban_Rural'] == 'Urban').sum()
rural_count = (df_normalized['Urban_Rural'] == 'Rural').sum()
print(f"   Created Urban_Rural: {urban_count:,} Urban, {rural_count:,} Rural")

# 4. Create derived metrics
print("\n4. Creating derived metrics...")
# Employment-Population ratio
if 'TotEmp' in df_normalized.columns and 'TotPop' in df_normalized.columns:
    df_normalized['Emp_Pop_Ratio'] = df_normalized['TotEmp'] / df_normalized['TotPop'].replace(0, np.nan)
    print("   Created Emp_Pop_Ratio")

# Workers per household
if 'Workers' in df_normalized.columns and 'HH' in df_normalized.columns:
    df_normalized['Workers_Per_HH'] = df_normalized['Workers'] / df_normalized['HH'].replace(0, np.nan)
    print("   Created Workers_Per_HH")

# ============================================================================
# SAVE CLEANED AND NORMALIZED DATA
# ============================================================================
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save cleaned data
output_file_clean = 'EPA_SmartLocationDatabase_V3_CLEANED.csv'
df_clean.to_csv(output_file_clean, index=False)
print(f"\n✓ Cleaned data saved to: {output_file_clean}")
print(f"  Shape: {df_clean.shape}")

# Save cleaned and normalized data
output_file_normalized = 'EPA_SmartLocationDatabase_V3_CLEANED_NORMALIZED.csv'
df_normalized.to_csv(output_file_normalized, index=False)
print(f"\n✓ Cleaned and normalized data saved to: {output_file_normalized}")
print(f"  Shape: {df_normalized.shape}")

# Create a data quality report
print("\n" + "="*80)
print("FINAL DATA QUALITY SUMMARY")
print("="*80)
print(f"\nOriginal dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Cleaned dataset: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")
print(f"Normalized dataset: {df_normalized.shape[0]:,} rows × {df_normalized.shape[1]} columns")
print(f"\nRows removed: {df.shape[0] - df_clean.shape[0]:,}")
print(f"New columns added: {df_normalized.shape[1] - df_clean.shape[1]}")

# Metro area summary
print("\n" + "="*80)
print("METRO AREA COVERAGE")
print("="*80)
print(f"Block groups in Combined Statistical Areas (CSA): {df_clean['In_CSA'].sum():,} ({(df_clean['In_CSA'].sum()/len(df_clean)*100):.1f}%)")
print(f"Block groups in Core Based Statistical Areas (CBSA): {df_clean['In_CBSA'].sum():,} ({(df_clean['In_CBSA'].sum()/len(df_clean)*100):.1f}%)")
print(f"Rural block groups (not in CBSA): {(df_clean['In_CBSA']==0).sum():,} ({((df_clean['In_CBSA']==0).sum()/len(df_clean)*100):.1f}%)")

# Summary statistics for key columns
print("\n" + "="*80)
print("KEY STATISTICS (Cleaned Data)")
print("="*80)
key_stats_cols = ['TotPop', 'TotEmp', 'Workers', 'HH', 'D1A', 'D1B', 'NatWalkInd']
existing_stats_cols = [col for col in key_stats_cols if col in df_clean.columns]
if existing_stats_cols:
    print(df_clean[existing_stats_cols].describe())

print("\n✓ Data cleaning and normalization complete!")
print("\nFiles created:")
print(f"  1. {output_file_clean}")
print(f"  2. {output_file_normalized}")
print("\nKey improvements:")
print("  • CSA and CBSA codes preserved as missing where appropriate")
print("  • Created In_CSA and In_CBSA binary indicators for analysis")
print("  • Created Urban_Rural classification based on CBSA membership")
print("  • All geographic identifiers properly formatted as strings")
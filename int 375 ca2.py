# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
sns.set(style='whitegrid')

# Load the dataset
file_path = "C:\\Users\\ACER\\Desktop\\CA2 INT375.csv"  # Updated path
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# View data structure
print("First 5 rows of the dataset:\n")
print(df.head())
print("\nColumn names:\n", df.columns)

# ------------------------------------------
# Objective 1: Distribution across Panchayats & Villages + HEATMAP
# ------------------------------------------
if 'panchayat_name' in df.columns and 'village_name' in df.columns:
    distribution = df.groupby(['panchayat_name', 'village_name']).size().reset_index(name='scheme_count')
    print("\nDistribution of schemes:\n", distribution.head())

    # Bar plot by Panchayat
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, y='panchayat_name', order=df['panchayat_name'].value_counts().index)
    plt.title('Water Supply Schemes by Panchayat')
    plt.xlabel('Number of Schemes')
    plt.ylabel('Panchayat')
    plt.tight_layout()
    plt.show()

    # Heatmap
    heatmap_data = df.groupby(['panchayat_name', 'village_name']).size().unstack(fill_value=0)
    plt.figure(figsize=(14, 10))
    sns.heatmap(heatmap_data, cmap='Blues', linewidths=0.5, linecolor='gray')
    plt.title('Heatmap of Scheme Distribution Across Panchayats and Villages')
    plt.xlabel('Village Name')
    plt.ylabel('Panchayat Name')
    plt.tight_layout()
    plt.show()
else:
    print("Panchayat or Village columns not found.")

# ------------------------------------------
# Objective 2: Financial Analysis
# ------------------------------------------
# Identify correct column names
print("\nAvailable columns for financial analysis:\n", df.columns)

# Try to find matching column names for cost/expenditure
cost_col = next((col for col in df.columns if 'estimated_cost' in col), None)
exp_col = next((col for col in df.columns if 'expenditure' in col), None)

if cost_col and exp_col:
    df[cost_col] = pd.to_numeric(df[cost_col], errors='coerce')
    df[exp_col] = pd.to_numeric(df[exp_col], errors='coerce')

    fin_df = df.dropna(subset=[cost_col, exp_col])
    fin_df['utilization_ratio'] = fin_df[exp_col] / fin_df[cost_col]

    print("\nBudget Utilization Statistics:\n", fin_df['utilization_ratio'].describe())

    plt.figure(figsize=(10, 6))
    sns.histplot(fin_df['utilization_ratio'], bins=20, kde=True)
    plt.axvline(1, color='red', linestyle='--', label='Fully Utilized')
    plt.title('Budget Utilization Ratio (Expenditure / Estimated Cost)')
    plt.xlabel('Utilization Ratio')
    plt.ylabel('Number of Schemes')
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("Financial columns not found.")

# ------------------------------------------
# Objective 3: Implementation Timeline
# ------------------------------------------
# Try to find matching date columns
comm_col = next((col for col in df.columns if 'commencement' in col), None)
comp_col = next((col for col in df.columns if 'completion' in col), None)

if comm_col and comp_col:
    df[comm_col] = pd.to_datetime(df[comm_col], errors='coerce')
    df[comp_col] = pd.to_datetime(df[comp_col], errors='coerce')
    df['duration_days'] = (df[comp_col] - df[comm_col]).dt.days

    print("\nProject Duration Statistics:\n", df['duration_days'].describe())

    plt.figure(figsize=(10, 6))
    sns.histplot(df['duration_days'].dropna(), bins=20, kde=True)
    plt.title('Implementation Duration of Schemes')
    plt.xlabel('Duration (Days)')
    plt.tight_layout()
    plt.show()
else:
    print("Commencement or Completion date columns not found.")

# ------------------------------------------
# Objective 4: Water Source Type Analysis
# ------------------------------------------
source_col = next((col for col in df.columns if 'source' in col), None)

if source_col:
    source_counts = df[source_col].value_counts()
    print("\nWater Source Type Frequency:\n", source_counts)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=source_counts.index, y=source_counts.values)
    plt.title('Types of Water Sources Used in Schemes')
    plt.ylabel('Number of Schemes')
    plt.xlabel('Water Source Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Source of Water column not found.")

# ------------------------------------------
# Objective 5: Geographical Coverage by Habitation
# ------------------------------------------
habit_col = next((col for col in df.columns if 'habitation_id' in col), None)

if habit_col:
    unique_habitations = df[habit_col].nunique()
    print(f"\nTotal Unique Habitations Covered: {unique_habitations}")

    habitation_counts = df[habit_col].value_counts()

    plt.figure(figsize=(12, 5))
    habitation_counts.head(10).plot(kind='bar')
    plt.title('Top 10 Habitations by Number of Schemes')
    plt.xlabel('Habitation ID')
    plt.ylabel('Scheme Count')
    plt.tight_layout()
    plt.show()
else:
    print("Habitation ID column not found.")

#yearwise scheme implementation
#Year-wise Scheme Implementation Trend
plt.figure()
scheme_per_year = df['sanction_year'].value_counts().sort_index()
sns.barplot(x=scheme_per_year.index, y=scheme_per_year.values, palette="viridis")
plt.title('Number of Schemes Sanctioned per Year')
plt.xlabel('Sanction Year')
plt.ylabel('Number of Schemes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#2 Scatter plot: Estimated Cost vs Expenditure
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='estimated_cost', y='expenditure', hue='source_type', alpha=0.7)
plt.title('Scatter Plot: Estimated Cost vs Expenditure')
plt.xlabel('Estimated Cost (in Crores)')
plt.ylabel('Expenditure (in Crores)')
plt.legend(title='Source Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
# Histogram of Estimated Cost
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.histplot(df['estimated_cost'], bins=30, color='steelblue', kde=True)
plt.title('Histogram: Distribution of Estimated Scheme Cost')
plt.xlabel('Estimated Cost (in Crores)')
plt.ylabel('Number of Schemes')
plt.tight_layout()
plt.show()
# Box plot: Expenditure by Source Type
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='source_type', y='expenditure', palette='pastel')
plt.title('Box Plot: Expenditure by Source Type')
plt.xlabel('Source Type')
plt.ylabel('Expenditure (in Crores)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
#6 line chart
yearly_schemes = df['sanction_year'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.lineplot(x=yearly_schemes.index, y=yearly_schemes.values, marker='o', color='teal')
plt.title('Line Chart: Number of Schemes Sanctioned Per Year')
plt.xlabel('Sanction Year')
plt.ylabel('Number of Schemes')
plt.grid(True)
#plt.tight_layo

# ------------------------------------------
# Summary
# ------------------------------------------
print("\nProject Analysis Complete")
print("Summary of Insights:")
print("- Schemes are unevenly distributed across panchayats and villages.")
print("- Budget utilization varies significantly across projects.")
print("- Many schemes are delayed beyond estimated timelines.")
print("- Deep Tubewells or similar water sources dominate usage.")
print("- Some habitations have more schemes, others are underserved.")

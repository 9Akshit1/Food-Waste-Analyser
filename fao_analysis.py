import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create a directory to save plots
os.makedirs("plots", exist_ok=True)

# Load the dataset
Data = pd.read_csv("FAO.csv")

# Drop duplicates
print("Number of duplicates:", Data.duplicated().sum())
Data = Data.drop_duplicates()

# Display head and count missing values
print(Data.head())
print(Data.isna().sum())

# Filter for specific countries and calculate mean loss percentage
selected_countries = [
    "Africa", "Asia", "Central Asia", "Europe", "Latin America and the Caribbean",
    "Northern Africa", "Northern America", "South-Eastern Asia", "Southern Asia",
    "Sub-Saharan Africa", "Western Africa", "Western Asia", "Australia and New Zealand", "World"
]

mean_loss = (
    Data[Data['country'].isin(selected_countries)]
    .groupby('country')['loss_percentage']
    .mean()
    .reset_index()
    .sort_values(by="loss_percentage", ascending=False)
)
print(mean_loss)

'''
# Boxplot of loss percentage by country
plt.figure(figsize=(10, 6))
sns.boxplot(data=Data[Data['country'].isin(selected_countries)], x="loss_percentage", y="country")
plt.title("Loss Percentage by Country")
plt.savefig("plots/loss_percentage_boxplot.png")
plt.close()

# Filter for specific conditions and sort by loss percentage
filtered_data = (
    Data[
        (Data['country'].isin(selected_countries)) &
        (Data['loss_percentage'] >= 20)
    ]
    .sort_values(by="loss_percentage", ascending=False)
    .loc[:, ["loss_percentage", "loss_percentage_original", "country", "commodity", "year", "food_supply_stage", "activity"]]
)
print(filtered_data)

# Mean loss percentage for countries not in the selected list
other_countries_mean_loss = (
    Data[~Data['country'].isin(selected_countries)]
    .groupby('country')['loss_percentage']
    .mean()
    .reset_index()
    .sort_values(by="loss_percentage", ascending=False)
)
print(other_countries_mean_loss)

# Filter for other countries with loss percentage >= 20
other_countries_filtered = (
    Data[
        (~Data['country'].isin(selected_countries)) &
        (Data['loss_percentage'] >= 20)
    ]
    .sort_values(by="loss_percentage", ascending=False)
    .loc[:, ["country", "commodity", "loss_percentage", "loss_percentage_original", "year", "food_supply_stage", "activity"]]
)
print(other_countries_filtered)

# Bar plot for food supply stage by country
n = 2
for country in selected_countries:
    subset = Data[(Data['country'] == country) & (Data['food_supply_stage'] != "")]
    if subset.empty:
        continue

    stage_mean_loss = (
        subset.groupby('food_supply_stage')['loss_percentage']
        .mean()
        .reset_index()
        .sort_values(by="loss_percentage", ascending=False)
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(data=stage_mean_loss, x="loss_percentage", y="food_supply_stage", palette="viridis")
    plt.title(f"Food Loss Percentage by Supply Stage in {country}")
    for index, row in stage_mean_loss.iterrows():
        plt.text(row['loss_percentage'], index, round(row['loss_percentage'], 2), va='center')
    plt.savefig(f"plots/food_loss_{country}.png")
    plt.close()
    n += 2

# Boxplot of loss percentage by food supply stage
plt.figure(figsize=(10, 6))
sns.boxplot(data=Data, x="loss_percentage", y="food_supply_stage")
plt.title("Loss Percentage by Food Supply Stage")
plt.savefig("plots/loss_percentage_food_stage_boxplot.png")
plt.close()

# Mean loss percentage by food supply stage
stage_mean_loss = (
    Data[Data['food_supply_stage'] != ""]
    .groupby('food_supply_stage')['loss_percentage']
    .mean()
    .reset_index()
    .sort_values(by="loss_percentage", ascending=False)
)
print(stage_mean_loss)

# Filter for Post-harvest stage with loss percentage >= 20
post_harvest_data = (
    Data[
        (~Data['country'].isin(selected_countries)) &
        (Data['loss_percentage'] >= 20) &
        (Data['food_supply_stage'] == "Post-harvest")
    ]
    .sort_values(by="loss_percentage", ascending=False)
    .loc[:, ["country", "commodity", "loss_percentage", "loss_percentage_original", "year", "food_supply_stage", "activity"]]
)
print(post_harvest_data)
'''

from scipy.stats import linregress

# Time series line graph for India
india_data = Data[Data['country'] == "India"]
# Calculate the mean for each year (you can change this to median if you prefer)
india_yearly_mean = india_data.groupby('year', as_index=False)['loss_percentage'].mean()

# Calculate the regression line slope and intercept
slope, intercept, r_value, p_value, std_err = linregress(india_yearly_mean['year'], india_yearly_mean['loss_percentage'])

# Print the slope of the regression line
print(f"Slope of the regression line: {slope}")

# Plotting the data with the regression line based on the mean for each year
plt.figure(figsize=(10, 6))
sns.regplot(data=india_yearly_mean, x="year", y="loss_percentage", scatter_kws={'s': 50}, line_kws={'color': 'red'}, ci=None)

# Title and labels
plt.title("Loss Percentage Over Years in India with Regression Line (Yearly Mean)")
plt.xlabel("Year")
plt.ylabel("Loss Percentage")

# Save the plot
plt.savefig("plots/india_loss_percentage_time_series_with_regression_mean.png")
plt.close()
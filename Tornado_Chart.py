# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(Item, Forecast_Volume, Actual_Volume)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
import numpy as np

# Power BI automatically provides your data as 'dataset'
df = dataset.copy()

# Rename columns for clarity (optional but helpful)
df.columns = ["Item", "Forecast_Volume", "Actual_Volume", "Accuracy", "Difference", "Region"]

# Sort data (optional: ascending by Accuracy)
df = df.sort_values("Accuracy", ascending=True).reset_index(drop=True)

# --- Normalize Accuracy for color mapping ---
accuracy = df["Accuracy"]
norm = (accuracy - accuracy.min()) / (accuracy.max() - accuracy.min())

# Limit the color intensity range (to keep hues soft)
norm_limited = np.clip(norm * 0.6 + 0.3, 0, 1)

# Define colormaps
cmap_actual = plt.cm.Reds
cmap_forecast = plt.cm.Blues

colors_actual = cmap_actual(norm_limited)
colors_forecast = cmap_forecast(norm_limited)

# --- Create Figure ---
fig, ax = plt.subplots(figsize=(9, 7))

# --- Plot Tornado Bars ---
bars_forecast = ax.barh(df["Item"], df["Forecast_Volume"], color=colors_forecast, label="Forecast")
bars_actual = ax.barh(df["Item"], -df["Actual_Volume"], color=colors_actual, label="Actual")
bars_diff = ax.barh(df["Item"], df["Difference"], color="seagreen", alpha=0.8, label="Difference")

# --- Add Labels for Forecast & Actual ---
for i, (actual, forecast) in enumerate(zip(df["Actual_Volume"], df["Forecast_Volume"])):
    offset = 0.09 * max(df["Forecast_Volume"].max(), df["Actual_Volume"].max())

    ax.text(
        -actual - offset, i, f"{actual:,}",
        va="center", ha="left", fontsize=8, color="black"
    )
    ax.text(
        forecast + offset, i, f"{forecast:,}",
        va="center", ha="right", fontsize=8, color="black"
    )

# --- Add Labels for Difference Bars ---
max_diff = max(abs(df["Difference"]))
for i, diff in enumerate(df["Difference"]):
    offset = 0.03 * max_diff
    align = "right" if diff < 0 else "left"
    x_pos = diff - offset if diff < 0 else diff + offset

    ax.text(
        x_pos, i, f"{abs(diff):,}",
        va="center", ha=align, fontsize=8, color="white", fontweight="bold"
    )

# --- Add Styling ---
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Volume", fontsize=10, labelpad=8)
ax.set_ylabel("Item", fontsize=10)
ax.set_title("Forecast vs Actual Sales (Tornado Chart)", fontsize=14, pad=15)

# --- Legends Setup ---
# Legend 1: Metrics
legend1 = ax.legend(
    handles=[bars_actual[0], bars_forecast[0], bars_diff[0]],
    labels=["Actual", "Forecast", "Difference"],
    loc="upper center",
    bbox_to_anchor=(0.5, -0.1),
    ncol=3,
    frameon=False
)

# --- Region Color Legend for Y-axis labels ---
region_colors = {
    "North": "#1f77b4",  # Blue
    "South": "#2ca02c",  # Green
    "East": "#ff7f0e",   # Orange
    "West": "#d62728"    # Red
}

# Color y-tick labels by region
yticklabels = ax.get_yticklabels()
for label, region in zip(yticklabels, df["Region"]):
    label.set_color(region_colors.get(region, "black"))

# Legend 2: Regions
region_handles = [
    plt.Line2D([0], [0], marker='o', color='w', label=region,
               markerfacecolor=color, markersize=8)
    for region, color in region_colors.items()
]

legend2 = ax.legend(
    handles=region_handles,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.16),
    ncol=len(region_handles),
    frameon=False
)

# Add both legends
ax.add_artist(legend1)

# --- Adjust Layout ---
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.subplots_adjust(bottom=0.25)
plt.show()
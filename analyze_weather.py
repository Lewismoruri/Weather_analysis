import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Load your data
df = pd.read_csv("weather.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ---- KPI Values ----
avg_temp = df["temperature"].mean()
avg_humidity = df["humidity"].mean()
common_condition = df["description"].mode()[0]

# ---- Dashboard Layout ----
fig = plt.figure(figsize=(14, 10))
grid = fig.add_gridspec(3, 2, height_ratios=[0.7, 1.5, 1.5])

# ------------------------------
# KPI PANELS (top row)
# ------------------------------
ax_kpi = fig.add_subplot(grid[0, :])
ax_kpi.axis("off")

def draw_kpi(ax, x, y, text, value, color):
    # Draw rectangle
    box = FancyBboxPatch((x, y), 0.25, 0.8,
                         boxstyle="round,pad=0.2,rounding_size=0.1",
                         linewidth=2, edgecolor=color, facecolor="white")
    ax.add_patch(box)
    # KPI Value
    ax.text(x + 0.125, y + 0.45, f"{value}", ha="center", va="center",
            fontsize=16, fontweight="bold", color=color)
    # KPI Label
    ax.text(x + 0.125, y + 0.15, text, ha="center", va="center",
            fontsize=12, color="black")

# Draw KPI tiles
draw_kpi(ax_kpi, 0.05, 0.1, "Avg Temp (°C)", f"{avg_temp:.1f}", "tomato")
draw_kpi(ax_kpi, 0.38, 0.1, "Avg Humidity (%)", f"{avg_humidity:.1f}", "royalblue")
draw_kpi(ax_kpi, 0.71, 0.1, "Most Common\nCondition", common_condition, "seagreen")

ax_kpi.set_xlim(0, 1)
ax_kpi.set_ylim(0, 1)

# ------------------------------
# Temperature Trends
# ------------------------------
ax1 = fig.add_subplot(grid[1, 0])
for city in df["city"].unique():
    city_data = df[df["city"] == city]
    ax1.plot(city_data["timestamp"], city_data["temperature"], marker="o", label=city)
ax1.set_title("🌡️ Temperature Trends", fontsize=12, fontweight="bold")
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature (°C)")
ax1.legend()

# ------------------------------
# Humidity Trends
# ------------------------------
ax2 = fig.add_subplot(grid[1, 1])
for city in df["city"].unique():
    city_data = df[df["city"] == city]
    ax2.plot(city_data["timestamp"], city_data["humidity"], marker="o", label=city)
ax2.set_title("💧 Humidity Trends", fontsize=12, fontweight="bold")
ax2.set_xlabel("Time")
ax2.set_ylabel("Humidity (%)")
ax2.legend()

# ------------------------------
# Avg Temp by City (bar)
# ------------------------------
ax3 = fig.add_subplot(grid[2, 0])
avg_temp_city = df.groupby("city")["temperature"].mean().sort_values()
avg_temp_city.plot(kind="bar", color="orange", ax=ax3)
ax3.set_title("Average Temperature by City", fontsize=12, fontweight="bold")
ax3.set_ylabel("Temperature (°C)")

# ------------------------------
# Weather Condition Distribution (pie)
# ------------------------------
ax4 = fig.add_subplot(grid[2, 1])
condition_counts = df["description"].value_counts()
ax4.pie(condition_counts, labels=condition_counts.index, autopct="%1.1f%%",
        startangle=90, colors=plt.cm.Paired.colors)
ax4.set_title("Weather Condition Distribution", fontsize=12, fontweight="bold")

# ------------------------------
# Final Touch
# ------------------------------
plt.suptitle("📊 Weather Dashboard", fontsize=16, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

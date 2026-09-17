import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Household Power Dashboard",
    layout="wide"
)

# Title
st.title("🏠 Household Power Consumption Dashboard")

# Load data
df = pd.read_csv("household_cleandata.csv")

# Sidebar
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

# Filter data
filtered_df = df[df["year"] == year]

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Power",
    round(filtered_df["Global_active_power"].mean(), 2)
)

col2.metric(
    "Average Voltage",
    round(filtered_df["Voltage"].mean(), 2)
)

col3.metric(
    "Average Intensity",
    round(filtered_df["Global_intensity"].mean(), 2)
)

st.divider()

# -------------------------------
# Graph 1: Power Consumption
# -------------------------------

st.subheader("Global Active Power")

hourly_power = (
    filtered_df.groupby("Hours")["Global_active_power"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    hourly_power["Hours"],
    hourly_power["Global_active_power"],
    marker="o"
)

ax.set_xlabel("Hour")
ax.set_ylabel("Average Global Active Power")
ax.set_title(f"Average Power Consumption by Hour - {year}")
ax.grid(True)

st.pyplot(fig)

# -------------------------------
# Graph 2: Voltage
# -------------------------------

st.subheader("Voltage by Hour")

hourly_voltage = (
    filtered_df.groupby("Hours")["Voltage"]
    .mean()
    .reset_index()
)

st.line_chart(
    hourly_voltage.set_index("Hours")
)

# -------------------------------
# Graph 3: Sub Metering
# -------------------------------

st.subheader("Sub Metering Consumption")

metering = filtered_df[
    ["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]
].mean()

st.bar_chart(metering)

# -------------------------------
# Data
# -------------------------------

st.subheader("Filtered Data")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.title("MLB Stats Interactive Dashboard")

@st.cache_data
def load_all_data():
    conn = sqlite3.connect("mlb_stats.db")
    cursor = conn.cursor()

    # Get all table names matching pattern 'table_%_1'
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'table_%_1'")
    tables = [row[0] for row in cursor.fetchall()]

    df_list = []
    for table in tables:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            df_list.append(df)
        except Exception as e:
            st.warning(f"Failed to load table {table}: {e}")

    conn.close()

    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df.columns = [col.strip() for col in combined_df.columns]
        return combined_df
    else:
        return pd.DataFrame()

df = load_all_data()

if df.empty:
    st.error("No data loaded from database.")
    st.stop()

# Show sample data
st.write("### Sample Data")
st.dataframe(df.head())

# Dropdown for year selection
years = sorted(df['year'].dropna().unique())
selected_year = st.selectbox("Select Year", years)

# Dropdown for statistic selection
if 'Statistic' in df.columns:
    stats = sorted(df['Statistic'].dropna().unique())
    selected_stat = st.selectbox("Select Statistic", stats)
else:
    st.error("Column 'Statistic' not found in data")
    st.stop()

# Filter data by year and statistic
filtered_df = df[(df['year'] == selected_year) & (df['Statistic'] == selected_stat)]

if filtered_df.empty:
    st.warning("No data available for this selection.")
    st.stop()

st.write(f"### Data for Year {selected_year} and Statistic '{selected_stat}'")
st.dataframe(filtered_df)

# Debug info
st.write("### Debug Info")
st.write("Filtered Data Length:", len(filtered_df))
st.write("Filtered Data Columns:", list(filtered_df.columns))

# Identify numeric column ('#' preferred, else '_')
num_col = None
if '#' in filtered_df.columns:
    num_col = '#'
elif '_' in filtered_df.columns:
    num_col = '_'

if num_col:
    filtered_df[num_col] = pd.to_numeric(filtered_df[num_col], errors='coerce')
    filtered_df = filtered_df.dropna(subset=[num_col])
else:
    st.info("No numeric column ('#' or '_') found in filtered data.")

# Visualization 1: Bar chart by player
if num_col and not filtered_df.empty:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sorted_df = filtered_df.sort_values(num_col, ascending=False)
    ax1.bar(sorted_df['Name'], sorted_df[num_col])
    ax1.set_xlabel("Player Name")
    ax1.set_ylabel(selected_stat)
    ax1.set_title(f"{selected_stat} by Player in {selected_year}")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)
else:
    st.info("No numeric data available for bar chart.")

# Visualization 2: Histogram of numeric values
if num_col and not filtered_df[num_col].isnull().all():
    fig2, ax2 = plt.subplots()
    ax2.hist(filtered_df[num_col], bins=15)
    ax2.set_title(f"Distribution of {selected_stat} in {selected_year}")
    ax2.set_xlabel(selected_stat)
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)
else:
    st.info("No numeric data available for histogram.")

# Visualization 3: Pie chart of teams
if 'Team' in filtered_df.columns:
    team_counts = filtered_df['Team'].value_counts()
    if not team_counts.empty:
        fig3, ax3 = plt.subplots()
        ax3.pie(team_counts, labels=team_counts.index, autopct='%1.1f%%', startangle=140)
        ax3.set_title(f"Team Distribution for {selected_stat} in {selected_year}")
        st.pyplot(fig3)
    else:
        st.info("No team data available to plot pie chart.")
else:
    st.info("Column 'Team' not found in data.")

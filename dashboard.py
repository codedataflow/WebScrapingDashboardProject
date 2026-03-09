"""
MLB Statistics Dashboard (2020–2025)
Interactive dashboard built with Streamlit.
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ------------------------------------------------
# Page setup
# ------------------------------------------------

st.set_page_config(page_title="MLB Stats Dashboard", layout="wide")

st.title("⚾ MLB Statistics Dashboard (2020–2025)")
st.write("Explore MLB player and team performance.")

# ------------------------------------------------
# Database connection
# ------------------------------------------------

conn = sqlite3.connect("mlb_stats.db")

# ------------------------------------------------
# Load data
# ------------------------------------------------

players = pd.read_sql_query("SELECT * FROM players", conn)
pitchers = pd.read_sql_query("SELECT * FROM pitchers", conn)
teams = pd.read_sql_query('SELECT * FROM team_standings', conn)

# ------------------------------------------------
# Sidebar filters
# ------------------------------------------------

years = sorted(players["Year"].unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

# ------------------------------------------------
# 1️⃣ Home Run Leaders
# ------------------------------------------------

st.subheader("Home Run Leaders")

home_runs = players[
    (players["Statistic"] == "Home Runs") &
    (players["Year"] == selected_year)
]

home_runs = home_runs.sort_values("#", ascending=False).head(10)

fig_hr = px.bar(
    home_runs,
    x="Name",
    y="#",
    color="Team",
    title=f"Top Home Run Hitters ({selected_year})"
)

st.plotly_chart(fig_hr, width="stretch")

# ------------------------------------------------
# 2️⃣ Batting Average Leaders
# ------------------------------------------------

st.subheader("Batting Average Leaders")

batting = players[
    (players["Statistic"] == "Batting Average") &
    (players["Year"] == selected_year)
]

#batting["#"] = batting["#"].astype(float)
batting.loc[:, "#"] = batting["#"].astype(float)

batting = batting.sort_values("#", ascending=False).head(10)

fig_avg = px.bar(
    batting,
    x="Name",
    y="#",
    color="Team",
    title=f"Top Batting Average ({selected_year})"
)

st.plotly_chart(fig_avg, width="stretch")

# ------------------------------------------------
# 3️⃣ Strikeout Leaders (Pitchers)
# ------------------------------------------------

st.subheader("Strikeout Leaders")

strikeouts = pitchers[
    pitchers["Statistic"].str.contains("Strike", case=False)
]

strikeouts = strikeouts[strikeouts["Year"] == selected_year]

strikeouts = strikeouts.sort_values("#", ascending=False).head(10)

fig_so = px.bar(
    strikeouts,
    x="Name",
    y="#",
    color="Team",
    title=f"Top Pitcher Strikeouts ({selected_year})"
)

st.plotly_chart(fig_so, width="stretch")

# ------------------------------------------------
# 4️⃣ Team Wins Comparison
# ------------------------------------------------

st.subheader("Team Wins")

teams_year = teams[teams["Year"] == selected_year]

fig_team = px.bar(
    teams_year,
    x="Team | Roster",
    y="W",
    title=f"Team Wins ({selected_year})"
)

st.plotly_chart(fig_team, width="stretch")

# ------------------------------------------------
# Close DB connection
# ------------------------------------------------

conn.close()

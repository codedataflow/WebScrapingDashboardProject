import sqlite3
import pandas as pd

# --------------------------------------------------
# Connect to database
# --------------------------------------------------

conn = sqlite3.connect("mlb_stats.db")

print("Connected to database\n")

# --------------------------------------------------
# 1. Home Run Leaders
# --------------------------------------------------

home_runs = pd.read_sql_query("""
SELECT Name,
       Team,
       Year,
       `#` AS HomeRuns
FROM players
WHERE Statistic = 'Home Runs'
ORDER BY HomeRuns DESC
""", conn)

print("HOME RUN LEADERS")
print(home_runs.head(10))
print()

# --------------------------------------------------
# 2. Batting Average Leaders
# --------------------------------------------------

batting_avg = pd.read_sql_query("""
SELECT Name,
       Team,
       Year,
       `#` AS BattingAverage
FROM players
WHERE Statistic = 'Batting Average'
ORDER BY BattingAverage DESC
""", conn)

print("BATTING AVERAGE LEADERS")
print(batting_avg.head(10))
print()

# --------------------------------------------------
# 3. Strikeout Leaders (Pitchers)
# --------------------------------------------------

strikeouts = pd.read_sql_query("""
SELECT Name,
       Team,
       Year,
       `#` AS Strikeouts
FROM pitchers
WHERE Statistic LIKE '%Strike%'
ORDER BY Strikeouts DESC
""", conn)

print("STRIKEOUT LEADERS")
print(strikeouts.head(10))
print()

# --------------------------------------------------
# 4. Team Standings
# --------------------------------------------------

teams = pd.read_sql_query("""
SELECT "Team | Roster" AS Team,
       W,
       L,
       WP,
       Year
FROM team_standings
ORDER BY W DESC
""", conn)

print("TEAM STANDINGS")
print(teams.head(10))
print()

# --------------------------------------------------
# Close connection
# --------------------------------------------------

conn.close()

print("Queries completed.")

import sqlite3
import pandas as pd

conn = sqlite3.connect("mlb_stats.db")

# players
players = pd.read_csv("data/players.csv")
players.to_sql("players", conn, if_exists="replace", index=False)

# pitchers
pitchers = pd.read_csv("data/pitchers.csv")
pitchers.to_sql("pitchers", conn, if_exists="replace", index=False)

# team standings
teams = pd.read_csv("data/team_standings.csv")
teams.to_sql("team_standings", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database successfully created.")

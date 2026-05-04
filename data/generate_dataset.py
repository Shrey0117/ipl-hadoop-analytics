"""
IPL Dataset Generator
Generates realistic IPL match and delivery data for Big Data Analytics demo
"""

import csv
import random
from datetime import date, timedelta

random.seed(42)

TEAMS = [
    "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Rajasthan Royals", "Delhi Capitals",
    "Sunrisers Hyderabad", "Punjab Kings"
]

VENUES = [
    "Wankhede Stadium", "MA Chidambaram Stadium", "Chinnaswamy Stadium",
    "Eden Gardens", "Sawai Mansingh Stadium", "Arun Jaitley Stadium",
    "Rajiv Gandhi International Stadium", "PCA Stadium"
]

CITIES = [
    "Mumbai", "Chennai", "Bangalore", "Kolkata",
    "Jaipur", "Delhi", "Hyderabad", "Mohali"
]

PLAYERS = {
    "Mumbai Indians":   ["Rohit Sharma", "Suryakumar Yadav", "Jasprit Bumrah", "Hardik Pandya", "Ishan Kishan"],
    "Chennai Super Kings": ["MS Dhoni", "Ruturaj Gaikwad", "Ravindra Jadeja", "Devon Conway", "Deepak Chahar"],
    "Royal Challengers Bangalore": ["Virat Kohli", "Faf du Plessis", "Glenn Maxwell", "Mohammed Siraj", "Dinesh Karthik"],
    "Kolkata Knight Riders": ["Shreyas Iyer", "Andre Russell", "Sunil Narine", "Venkatesh Iyer", "Rinku Singh"],
    "Rajasthan Royals": ["Sanju Samson", "Jos Buttler", "Yuzvendra Chahal", "Ravichandran Ashwin", "Shimron Hetmyer"],
    "Delhi Capitals":   ["David Warner", "Prithvi Shaw", "Axar Patel", "Kuldeep Yadav", "Rishabh Pant"],
    "Sunrisers Hyderabad": ["Kane Williamson", "Aiden Markram", "Bhuvneshwar Kumar", "T Natarajan", "Heinrich Klaasen"],
    "Punjab Kings":     ["Shikhar Dhawan", "Jonny Bairstow", "Arshdeep Singh", "Liam Livingstone", "Sam Curran"]
}

# ─── Generate matches.csv ───────────────────────────────────────────────────

matches = []
match_id = 1
start_date = date(2020, 9, 19)

for season in range(2020, 2024):
    for match_num in range(60):
        teams_sample = random.sample(TEAMS, 2)
        team1, team2 = teams_sample
        venue_idx = random.randint(0, len(VENUES) - 1)
        toss_winner = random.choice([team1, team2])
        toss_decision = random.choice(["bat", "field"])

        # 55% chance toss winner wins (slight correlation)
        if random.random() < 0.55:
            winner = toss_winner
        else:
            winner = team2 if toss_winner == team1 else team1

        win_type = random.choice(["runs", "wickets"])
        win_margin = random.randint(6, 78) if win_type == "runs" else random.randint(1, 9)

        match_date = start_date + timedelta(days=match_num * 3 + (season - 2020) * 200)
        city = CITIES[venue_idx]
        potm = random.choice(PLAYERS[winner])  # Player of the Match from winning team

        matches.append([
            match_id, season, match_date.strftime("%Y-%m-%d"), city,
            VENUES[venue_idx], team1, team2,
            toss_winner, toss_decision, winner,
            win_margin if win_type == "runs" else 0,
            win_margin if win_type == "wickets" else 0,
            potm
        ])
        match_id += 1

with open("data/matches.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "match_id", "season", "date", "city", "venue",
        "team1", "team2", "toss_winner", "toss_decision", "winner",
        "win_by_runs", "win_by_wickets", "player_of_match"
    ])
    writer.writerows(matches)

print(f"✅ matches.csv created — {len(matches)} matches")

# ─── Generate deliveries.csv ────────────────────────────────────────────────

deliveries = []
delivery_id = 1

for m in matches[:100]:   # Generate deliveries for first 100 matches to keep size manageable
    mid = m[0]
    batting_team = m[5]   # team1 bats first (simplified)
    bowling_team = m[6]

    for inning in [1, 2]:
        if inning == 2:
            batting_team, bowling_team = bowling_team, batting_team

        batters = PLAYERS[batting_team][:3]
        bowlers = PLAYERS[bowling_team][2:5]

        for over in range(1, 21):
            for ball in range(1, 7):
                batsman = random.choice(batters)
                bowler  = random.choice(bowlers)
                runs_b  = random.choices([0, 1, 2, 4, 6], weights=[35, 30, 15, 12, 8])[0]
                extras  = random.choices([0, 1], weights=[90, 10])[0]
                total   = runs_b + extras
                is_wicket = 1 if (random.random() < 0.04 and over > 2) else 0
                dismissal = random.choice(["caught", "bowled", "lbw", "run out"]) if is_wicket else ""

                deliveries.append([
                    delivery_id, mid, inning, batting_team, bowling_team,
                    over, ball, batsman, bowler, runs_b, extras, total,
                    is_wicket, dismissal
                ])
                delivery_id += 1

with open("data/deliveries.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "delivery_id", "match_id", "inning", "batting_team", "bowling_team",
        "over", "ball", "batsman", "bowler", "batsman_runs", "extras",
        "total_runs", "is_wicket", "dismissal_kind"
    ])
    writer.writerows(deliveries)

print(f"✅ deliveries.csv created — {len(deliveries)} delivery records")
print("\nDataset generation complete!")
print(f"  matches.csv    : {len(matches):,} rows")
print(f"  deliveries.csv : {len(deliveries):,} rows")

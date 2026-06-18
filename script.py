import requests
import json
import os

API_KEY = os.getenv("ODDS_API_KEY", "ed66d37a72609bc89429815486b22117")

# Partidos del Mundial desde Football-Data
url_fd = "https://api.football-data.org/v4/competitions/WC/matches"
headers_fd = {"X-Auth-Token": os.getenv("FOOTBALL_DATA_KEY")}
response_fd = requests.get(url_fd, headers=headers_fd)

if response_fd.status_code != 200:
    print("Error Football-Data:", response_fd.status_code, response_fd.text)
    exit()

matches_fd = response_fd.json().get("matches", [])

# Cuotas desde OddsAPI
url_odds = "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
params_odds = {
    "apiKey": API_KEY,
    "regions": "eu",
    "markets": "h2h,spreads,totals"
}
response_odds = requests.get(url_odds, params=params_odds)

if response_odds.status_code != 200:
    print("Error OddsAPI:", response_odds.status_code, response_odds.text)
    exit()

odds_data = response_odds.json()

dashboard = []

for match in matches_fd:
    home = match.get("homeTeam", {}).get("name")
    away = match.get("awayTeam", {}).get("name")

    # Saltar partidos sin nombres válidos
    if not home or not away:
        continue

    # Buscar cuotas correspondientes en OddsAPI
    odds_match = next(
        (o for o in odds_data if home in o.get("home_team", "") and away in o.get("away_team", "")),
        None
    )

    odds_block = {}
    if odds_match:
        odds_block["bookmakers"] = odds_match.get("bookmakers", [])
        # Extraer mercados principales
        for bookmaker in odds_match.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] == "h2h":
                    outcomes = {o["name"]: o["price"] for o in market["outcomes"]}
                    odds_block["home_win"] = outcomes.get(home)
                    odds_block["away_win"] = outcomes.get(away)
                    odds_block["draw"] = outcomes.get("Draw")
                elif market["key"] == "totals":
                    odds_block["over_under"] = [
                        {"name": o["name"], "line": o["point"], "price": o["price"]}
                        for o in market["outcomes"]
                    ]
                elif market["key"] == "spreads":
                    odds_block["handicap"] = [
                        {"name": o["name"], "line": o["point"], "price": o["price"]}
                        for o in market["outcomes"]
                    ]

    # Datos ficticios de H2H y stats (puedes reemplazar con AiScore)
    h2h_data = {"total_matches": 5, "home_wins": 2, "away_wins": 2, "draws": 1}
    stats_data = {"home_goals": 10, "away_goals": 8}

    dashboard.append({
        "fecha": match.get("utcDate"),
        "home": home,
        "away": away,
        "estado": match.get("status"),
        "h2h": h2h_data,
        "stats": stats_data,
        "odds": odds_block
    })

with open("dashboard.json", "w", encoding="utf-8") as f:
    json.dump(dashboard, f, indent=2, ensure_ascii=False)

print("Guardados", len(dashboard), "partidos con cuotas reales y varios bookmakers en dashboard.json")

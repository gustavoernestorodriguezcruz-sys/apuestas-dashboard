import requests
import json
import os

# Usa tu API key de OddsAPI
API_KEY = os.getenv("ODDS_API_KEY", "ed66d37a72609bc89429815486b22117")

# 1. Obtener partidos del Mundial 2026 desde Football-Data
url_fd = "https://api.football-data.org/v4/competitions/WC/matches"
headers_fd = {"X-Auth-Token": os.getenv("FOOTBALL_DATA_KEY")}
response_fd = requests.get(url_fd, headers=headers_fd)

if response_fd.status_code != 200:
    print("Error Football-Data:", response_fd.status_code, response_fd.text)
    exit()

matches_fd = response_fd.json().get("matches", [])

dashboard = []

# 2. Obtener cuotas reales desde OddsAPI
url_odds = f"https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
params_odds = {
    "apiKey": API_KEY,
    "regions": "eu",          # Europa
    "markets": "h2h,spreads,totals"  # 1X2, hándicap, over/under
}
response_odds = requests.get(url_odds, params=params_odds)

if response_odds.status_code != 200:
    print("Error OddsAPI:", response_odds.status_code, response_odds.text)
    exit()

odds_data = response_odds.json()

# 3. Mapear partidos con cuotas
for match in matches_fd:
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    # Buscar cuotas correspondientes en OddsAPI
    odds_match = next(
        (o for o in odds_data if home in o["home_team"] and away in o["away_team"]),
        None
    )

    odds_block = {}
    if odds_match:
        # Extraer mercados principales
        for bookmaker in odds_match.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] == "h2h":  # 1X2
                    outcomes = {o["name"]: o["price"] for o in market["outcomes"]}
                    odds_block["home_win"] = outcomes.get(home)
                    odds_block["away_win"] = outcomes.get(away)
                    odds_block["draw"] = outcomes.get("Draw")
                elif market["key"] == "totals":  # Over/Under
                    odds_block["over_under"] = [
                        {"name": o["name"], "line": o["point"], "price": o["price"]}
                        for o in market["outcomes"]
                    ]
                elif market["key"] == "spreads":  # Hándicap
                    odds_block["handicap"] = [
                        {"name": o["name"], "line": o["point"], "price": o["price"]}
                        for o in market["outcomes"]
                    ]

    # H2H y stats ficticios (puedes reemplazar con AiScore)
    h2h_data = {"total_matches": 5, "home_wins": 2, "away_wins": 2, "draws": 1}
    stats_data = {"home_goals": 10, "away_goals": 8}

    dashboard.append({
        "fecha": match["utcDate"],
        "home": home,
        "away": away,
        "estado": match["status"],
        "h2h": h2h_data,
        "stats": stats_data,
        "odds": odds_block
    })

# 4. Guardar todo en dashboard.json
with open("dashboard.json", "w", encoding="utf-8") as f:
    json.dump(dashboard, f, indent=2, ensure_ascii=False)

print("Guardados", len(dashboard), "partidos con cuotas reales en dashboard.json")

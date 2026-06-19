import os
import requests
import json
from datetime import datetime

FOOTBALL_DATA_KEY = os.getenv("FOOTBALL_DATA_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

def get_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Error en Football-Data: {resp.status_code}")
        return []
    data = resp.json()
    matches = []
    for m in data.get("matches", []):
        matches.append({
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"],
            "fecha": m["utcDate"],
            "estado": m["status"].lower().replace("_", "")  # Normalizar estados
        })
    print(f"✓ {len(matches)} partidos obtenidos de Football-Data")
    return matches

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds/?regions=eu&markets=h2h,totals,spreads&apiKey={ODDS_API_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"❌ Error en OddsAPI: {resp.status_code}")
        return {}
    data = resp.json()
    odds_map = {}
    for game in data:
        home = game["home_team"]
        away = game["away_team"]
        key = f"{home}-{away}"
        odds_map[key] = {"bookmakers": []}

        # H2H
        for bm in game.get("bookmakers", []):
            bm_entry = {"title": bm["title"], "markets": []}
            for market in bm.get("markets", []):
                if market["key"] == "h2h":
                    outcomes = []
                    for o in market["outcomes"]:
                        if o["name"] == home:
                            odds_map[key]["home_win"] = o["price"]
                        elif o["name"] == away:
                            odds_map[key]["away_win"] = o["price"]
                        elif o["name"].lower() == "draw":
                            odds_map[key]["draw"] = o["price"]
                        outcomes.append({"name": o["name"], "price": o["price"]})
                    bm_entry["markets"].append({"outcomes": outcomes})
                elif market["key"] == "totals":
                    totals = []
                    for o in market["outcomes"]:
                        totals.append({"name": o["name"], "line": o["point"], "price": o["price"]})
                    odds_map[key].setdefault("over_under", totals)
                elif market["key"] == "spreads":
                    spreads = []
                    for o in market["outcomes"]:
                        spreads.append({"name": o["name"], "line": o["point"], "price": o["price"]})
                    odds_map[key].setdefault("handicap", spreads)
            odds_map[key]["bookmakers"].append(bm_entry)
    print(f"✓ {len(odds_map)} matches con odds encontrados en OddsAPI")
    return odds_map

def main():
    matches = get_matches()
    odds_map = get_odds()
    dashboard = []
    
    matches_without_odds = []
    for m in matches:
        key = f"{m['home']}-{m['away']}"
        match_data = m
        if key in odds_map:
            match_data["odds"] = odds_map[key]
        else:
            match_data["odds"] = {}
            matches_without_odds.append(key)
        dashboard.append(match_data)
    
    # Debug: Reportar partidos sin odds
    if matches_without_odds:
        print(f"⚠️ {len(matches_without_odds)} partidos SIN odds:")
        for m in matches_without_odds:
            print(f"   - {m}")
    else:
        print("✓ Todos los partidos tienen odds disponibles")

    with open("dashboard.json", "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
    print("✓ dashboard.json guardado exitosamente")

if __name__ == "__main__":
    main()

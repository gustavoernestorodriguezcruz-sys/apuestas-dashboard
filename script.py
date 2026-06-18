import requests
import json
import os

API_KEY = os.getenv("FOOTBALL_DATA_KEY")

# 1. Obtener partidos del Mundial 2026
url = "https://api.football-data.org/v4/competitions/WC/matches"
headers = {"X-Auth-Token": API_KEY}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit()

data = response.json()
matches = data.get("matches", [])

dashboard = []

# 2. Generar datos con H2H ficticio + stats + odds
for match in matches:
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    # Ejemplo de H2H simulado
    h2h_data = {
        "total_matches": 5,
        "home_wins": 2,
        "away_wins": 2,
        "draws": 1
    }

    # Ejemplo de estadísticas simuladas
    stats_data = {
        "home_goals": 10,
        "away_goals": 8
    }

    # ⚠️ Odds ficticias (puedes reemplazar con datos reales de MiCasino/AiScore)
    odds_data = {
        "home_win": 2.1,
        "draw": 3.4,
        "away_win": 2.8
    }

    dashboard.append({
        "fecha": match["utcDate"],
        "home": home,
        "away": away,
        "estado": match["status"],
        "h2h": h2h_data,
        "stats": stats_data,
        "odds": odds_data
    })

# 3. Guardar todo en dashboard.json
with open("dashboard.json", "w", encoding="utf-8") as f:
    json.dump(dashboard, f, indent=2, ensure_ascii=False)

print("Guardados", len(dashboard), "partidos en dashboard.json")

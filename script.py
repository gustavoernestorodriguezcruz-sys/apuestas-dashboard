import requests, json, os

API_KEY = os.getenv("FOOTBALL_DATA_KEY")
url = "https://api.football-data.org/v4/competitions/WC/matches"  # Mundial 2026

headers = {"X-Auth-Token": API_KEY}
response = requests.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()
    partidos = []
    for match in data.get("matches", []):
        partidos.append({
            "id": match["id"],
            "competicion": match["competition"]["name"],
            "home": match["homeTeam"]["name"],
            "away": match["awayTeam"]["name"],
            "fecha": match["utcDate"],
            "estado": match["status"]
        })
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(partidos, f, indent=2, ensure_ascii=False)
    print("Guardados", len(partidos), "partidos en data.json")
else:
    print("Error:", response.status_code, response.text)

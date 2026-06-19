import json

def implied_probabilities(odds):
    # Validar que existan las claves necesarias
    required_keys = ["home_win", "draw", "away_win"]
    if not all(key in odds and odds[key] for key in required_keys):
        return None  # saltar si faltan cuotas

    inv_home = 1 / odds["home_win"]
    inv_draw = 1 / odds["draw"]
    inv_away = 1 / odds["away_win"]

    total = inv_home + inv_draw + inv_away

    p_home = inv_home / total
    p_draw = inv_draw / total
    p_away = inv_away / total

    return {
        "prob_home": round(p_home, 2),
        "prob_draw": round(p_draw, 2),
        "prob_away": round(p_away, 2)
    }

def match_prediction(odds):
    probs = implied_probabilities(odds)
    if not probs:
        return None  # no se puede calcular

    ev_home = probs["prob_home"] * odds["home_win"]
    ev_draw = probs["prob_draw"] * odds["draw"]
    ev_away = probs["prob_away"] * odds["away_win"]

    evs = {"home": ev_home, "draw": ev_draw, "away": ev_away}
    best_key = max(evs, key=evs.get)
    best_ev = evs[best_key]
    
    # Solo recomendar si EV > 1.0, de lo contrario "PASS"
    recommendation = best_key if best_ev > 1.0 else "PASS"

    return {
        **probs,
        "ev_home": round(ev_home, 2),
        "ev_draw": round(ev_draw, 2),
        "ev_away": round(ev_away, 2),
        "recommendation": recommendation,
        "best_ev": round(best_ev, 2)
    }

if __name__ == "__main__":
    with open("dashboard.json", encoding="utf-8") as f:
        matches = json.load(f)

    for m in matches:
        odds = m.get("odds", {})
        pred = match_prediction(odds)
        if pred:
            m["prediction"] = pred
        else:
            # Aviso cuando no hay datos suficientes
            m["prediction"] = {"recommendation": "⚠️ Sin datos"}

    with open("dashboard.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)

    print("✓ Predicciones añadidas a dashboard.json")

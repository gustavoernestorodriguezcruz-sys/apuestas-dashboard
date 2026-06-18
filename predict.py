import json

def implied_probabilities(odds):
    # Convertir cuotas a probabilidades implícitas
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

    # Valor esperado simple = probabilidad * cuota
    ev_home = probs["prob_home"] * odds["home_win"]
    ev_draw = probs["prob_draw"] * odds["draw"]
    ev_away = probs["prob_away"] * odds["away_win"]

    return {
        **probs,
        "ev_home": round(ev_home, 2),
        "ev_draw": round(ev_draw, 2),
        "ev_away": round(ev_away, 2),
        "recommendation": max(
            [("home", ev_home), ("draw", ev_draw), ("away", ev_away)],
            key=lambda x: x[1]
        )[0]
    }

if __name__ == "__main__":
    with open("dashboard.json") as f:
        matches = json.load(f)

    for m in matches:
        if "odds" not in m:
            continue
        pred = match_prediction(m["odds"])
        m["prediction"] = pred

    with open("dashboard.json", "w") as f:
        json.dump(matches, f, indent=2)

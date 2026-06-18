import json
import math

def poisson_prob(lam, k):
    """Probabilidad de k goles con media lam (Poisson)."""
    return (lam**k * math.exp(-lam)) / math.factorial(k)

def match_prediction(home_goals_avg, away_goals_avg, odds):
    # Probabilidades simplificadas
    p_home = poisson_prob(home_goals_avg, 1)
    p_draw = poisson_prob((home_goals_avg + away_goals_avg) / 2, 1)
    p_away = poisson_prob(away_goals_avg, 1)

    # Valor esperado (EV)
    ev_home = p_home * odds["home_win"]
    ev_draw = p_draw * odds["draw"]
    ev_away = p_away * odds["away_win"]

    return {
        "prob_home": round(p_home, 2),
        "prob_draw": round(p_draw, 2),
        "prob_away": round(p_away, 2),
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
        pred = match_prediction(
            m["stats"]["home_goals"],
            m["stats"]["away_goals"],
            m["odds"]
        )
        m["prediction"] = pred

    with open("dashboard.json", "w") as f:
        json.dump(matches, f, indent=2)

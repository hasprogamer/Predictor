# Supposons que tu as un dictionnaire contenant les résultats par fiabilité
resultats_par_fiabilite = {
    91: {"gagné": 3, "total": 4, "cote_moy": 2.8},
    78: {"gagné": 6, "total": 9, "cote_moy": 3.1},
    65: {"gagné": 8, "total": 12, "cote_moy": 2.5},
    45: {"gagné": 10, "total": 25, "cote_moy": 3.0},
}

# Tranches regroupées
tranches = {
    ">=90": {"min": 90, "min_paris": 5, "gagné": 0, "total": 0, "cotes": []},
    ">=75": {"min": 75, "min_paris": 10, "gagné": 0, "total": 0, "cotes": []},
    ">=60": {"min": 60, "min_paris": 10, "gagné": 0, "total": 0, "cotes": []},
    ">=0":  {"min": 0,  "min_paris": 15, "gagné": 0, "total": 0, "cotes": []},
}

# Regrouper les résultats
for fiab, data in resultats_par_fiabilite.items():
    for label, tranche in tranches.items():
        if fiab >= tranche["min"]:
            tranche["gagné"] += data["gagné"]
            tranche["total"] += data["total"]
            tranche["cotes"].append(data["cote_moy"])
            break

print("=== Proposition automatique de % de mise (Kelly) ===")
for label, data in tranches.items():
    if data["total"] >= data["min_paris"]:
        winrate = data["gagné"] / data["total"]
        cote_moy = sum(data["cotes"]) / len(data["cotes"])
        proba = winrate
        mise = max((proba * (cote_moy - 1) - (1 - proba)) / (cote_moy - 1), 0)
        mise_percent = round(mise * 100, 2)
        print(f"{label} → {mise_percent}% du capital")
    else:
        print(f"{label} → Données insuffisantes ({data['total']} paris)")

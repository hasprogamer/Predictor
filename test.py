import json, os

# — chemins vers les fichiers —
HISTO_FILE   = "historique_matchs.json"
PROFILS_FILE = "profils.json"

# — paramètres de chaque bucket —
BUCKETS = [
    {"label": ">=90", "min": 90, "max": 101, "min_paris": 5},
    {"label": ">=75", "min": 75, "max": 90,  "min_paris": 10},
    {"label": ">=60", "min": 60, "max": 75,  "min_paris": 10},
    {"label": ">=0",  "min": 0,  "max": 60,  "min_paris": 15},
]

# — utilitaires de chargement/sauvegarde —
def charger_histo():
    if os.path.exists(HISTO_FILE):
        with open(HISTO_FILE, 'r') as f:
            return json.load(f).get("historique", [])
    return []

def charger_profils():
    if os.path.exists(PROFILS_FILE):
        with open(PROFILS_FILE, 'r') as f:
            return json.load(f)
    return {"profils": {}, "profil_actif": None}

def sauvegarder_profils(profils):
    with open(PROFILS_FILE, 'w') as f:
        json.dump(profils, f, indent=4)

# — calcul des stats pour un bucket donné —
def stats_bucket(histo, min_f, max_f):
    wins = total = 0
    sum_odds = 0.0
    for m in histo:
        f = m.get("fiabilite", -1)
        if f >= min_f and f < max_f:
            total += 1
            sum_odds += m.get("cote", 0)
            if m.get("resultat") == "GAGNÉ":
                wins += 1
    if total == 0:
        return {"wins": 0, "total": 0, "win_rate": 0.0, "avg_odds": 0.0}
    return {
        "wins": wins,
        "total": total,
        "win_rate": wins / total,
        "avg_odds": sum_odds / total
    }

# — fraction de Kelly (clipée entre 0 et 0.5) —
def kelly_fraction(p, b):
    if b <= 0:
        return 0.0
    f = (p * b - (1 - p)) / b
    return max(0.0, min(f, 0.5))

def main():
    # 1) charger historique et profils
    histo = charger_histo()
    if not histo:
        print("Aucun historique trouvé.")
        return

    profils = charger_profils()
    actif = profils.get("profil_actif")
    if not actif or actif not in profils["profils"]:
        print("⚠️ Aucun profil actif à mettre à jour.")
        return

    profil = profils["profils"][actif]

    # 2) calcul des nouvelles mises
    nouveau_profil = {}
    print("=== Calcul automatique des % de mise ===")
    for bucket in BUCKETS:
        label = bucket["label"]
        s = stats_bucket(histo, bucket["min"], bucket["max"])
        if s["total"] >= bucket["min_paris"]:
            p = s["win_rate"]
            b = s["avg_odds"] - 1
            f = kelly_fraction(p, b)
            pct = round(f * 100, 2)
            print(f"{label} : {s['wins']}/{s['total']} gains → {p*100:.1f}% | cote moy. {s['avg_odds']:.2f} → mise {pct}%")
            nouveau_profil[label] = pct
        else:
            ancien = profil.get(label, 0.0)
            print(f"{label} : données insuffisantes ({s['total']} < {bucket['min_paris']}) → on garde {ancien}%")
            nouveau_profil[label] = ancien

    # 3) affichage comparatif et confirmation
    print(f"\nProfil actif : '{actif}'. Comparaison ancien / nouveau :")
    for label in [b["label"] for b in BUCKETS]:
        ancien = profil.get(label, 0.0)
        nouveau = nouveau_profil[label]
        print(f"  • {label} : {ancien}% → {nouveau}%")

    choix = input("\nAppliquer ces changements au profil ? (o/n) : ").strip().lower()
    if choix == 'o':
        profils["profils"][actif] = nouveau_profil
        sauvegarder_profils(profils)
        print(f"\n✅ Profil '{actif}' mis à jour dans {PROFILS_FILE}.")
    else:
        print("\n🚫 Aucune modification appliquée.")

if __name__ == "__main__":
    main()

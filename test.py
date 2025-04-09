import json, os

# — fichiers —
HISTO_FILE   = "historique_matchs.json"
PROFILS_FILE = "profils.json"

# — chargement / sauvegarde —
def charger_histo():
    if os.path.exists(HISTO_FILE):
        with open(HISTO_FILE,'r') as f:
            return json.load(f).get("historique",[])
    return []

def charger_profils():
    if os.path.exists(PROFILS_FILE):
        with open(PROFILS_FILE,'r') as f:
            return json.load(f)
    return {"profils":{}, "profil_actif":None}

def sauvegarder_profils(profils):
    with open(PROFILS_FILE,'w') as f:
        json.dump(profils,f,indent=4)

# — stats par fiabilité (wins, total, win_rate, avg_odds) —
def calcul_stats(histo):
    stats = {}
    for m in histo:
        fiab = m.get("fiabilite")
        cote = m.get("cote", 0)
        if fiab is None or cote <= 1: continue
        s = stats.setdefault(fiab, {"wins":0,"total":0,"sum_odds":0.0})
        s["total"] += 1
        s["sum_odds"] += cote
        if m.get("resultat")=="GAGNÉ":
            s["wins"] += 1
    # calculer win_rate et avg_odds
    for fiab,s in stats.items():
        s["win_rate"] = s["wins"]/s["total"]
        s["avg_odds"] = s["sum_odds"]/s["total"]
    return stats

# — Kelly fraction —
def kelly_fraction(p, b):
    f = (p*(b) - (1-p)) / b
    return max(0.0, min(f, 0.5))  # clip entre 0 et 0.5

# — proposition automatique de nouveau profil —
def proposer_nouveau_profil(stats):
    nouveau = {}
    for fiab, s in stats.items():
        p = s["win_rate"]
        b = s["avg_odds"] - 1
        f = kelly_fraction(p, b)
        pct = round(f*100,2)
        nouveau[f">={fiab}"] = pct
    return nouveau

# — affichage des stats et proposition —
def main():
    histo = charger_histo()
    if not histo:
        print("Aucun historique trouvé.")
        return

    stats = calcul_stats(histo)
    if not stats:
        print("Aucune fiabilité valide dans l’historique.")
        return

    print("=== Statistiques et cotes moyennes par fiabilité ===")
    for fiab in sorted(stats.keys(), reverse=True):
        s = stats[fiab]
        print(f"Fiabilité {fiab}% : {s['wins']}/{s['total']} gains → {s['win_rate']*100:.1f}% | cote moy. {s['avg_odds']:.2f}")

    # calcul automatique
    nouveau = proposer_nouveau_profil(stats)
    print("\n=== Proposition automatique de % de mise (Kelly) ===")
    for seuil,pct in sorted(nouveau.items(), reverse=True):
        print(f"{seuil} → {pct}% du capital")

    # chargement profil actif
    profils = charger_profils()
    actif = profils.get("profil_actif")
    if not actif or actif not in profils["profils"]:
        print("\n⚠️ Aucun profil actif à mettre à jour.")
        return

    # confirmation utilisateur
    print(f"\nProfil actif : '{actif}'.")
    rep = input("Veux‑tu appliquer ces nouveaux pourcentages ? (o/n) : ").strip().lower()
    if rep == 'o':
        profils["profils"][actif] = nouveau
        sauvegarder_profils(profils)
        print("✅ Profil mis à jour.")
    else:
        print("Aucun changement appliqué.")

if __name__=="__main__":
    main()

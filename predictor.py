import time
import json
import os

# Fichiers de données
historique_fichier = "historique_paris.txt"
profils_fichier = "profils.json"
historique_matchs_fichier = "historique_matchs.json"
bankroll_fichier = "bankroll.json"

# — Gestion des profils —
def charger_profils():
    if os.path.exists(profils_fichier):
        with open(profils_fichier, 'r') as f:
            return json.load(f)
    return {"profils": {}, "profil_actif": None}

def sauvegarder_profils(profils):
    with open(profils_fichier, 'w') as f:
        json.dump(profils, f, indent=4)

# — Entraînement local simple —
def charger_historique_matchs():
    if os.path.exists(historique_matchs_fichier):
        with open(historique_matchs_fichier, 'r') as f:
            return json.load(f)
    return {"historique": []}

def sauvegarder_historique_matchs(histo):
    with open(historique_matchs_fichier, 'w') as f:
        json.dump(histo, f, indent=4)

def entrainement_local(equipes, score, fiabilite, resultat, cote, pari_type):
    histo = charger_historique_matchs()
    histo["historique"].append({
        "equipes": equipes,
        "score": score,
        "fiabilite": fiabilite,
        "resultat": resultat,
        "cote": cote,
        "pari_type": pari_type
    })
    sauvegarder_historique_matchs(histo)

# — Suivi de bankroll & gestion du risque —
def charger_bankroll():
    if os.path.exists(bankroll_fichier):
        with open(bankroll_fichier, 'r') as f:
            return json.load(f)
    return {"capital_initial": 10000, "capital_actuel": 10000}

def sauvegarder_bankroll(bankroll):
    with open(bankroll_fichier, 'w') as f:
        json.dump(bankroll, f, indent=4)

def suivre_bankroll(mise, gain, perte):
    bankroll = charger_bankroll()
    bankroll["capital_actuel"] += gain - perte
    sauvegarder_bankroll(bankroll)

def kelly_criterion(probabilite, cote, capital):
    return int(capital * (probabilite * (cote - 1) - (1 - probabilite)) / (cote - 1))

# — Code existant préservé —  
def moyenne_ponderee(scores):
    poids = [1, 1, 1, 2, 2]
    if len(scores) != 5:
        raise ValueError("Il faut exactement 5 valeurs")
    total = sum(s * p for s, p in zip(scores, poids))
    return round(total / sum(poids), 2)

def score_fiabilite(pts_1h, pts_match):
    return min(100, int((pts_1h + pts_match) * 7))

def demande_scores(nom_equipe):
    print(f"\nEntrez les scores des 5 derniers matchs pour {nom_equipe} :")
    return [int(input(f"Match {i+1} : ")) for i in range(5)]

def suggere_mise(fiabilite, solde, profil_actif, profils):
    profil = profils["profils"].get(profil_actif, {})
    # on parcourt les paliers du profil
    for seuil_str, pct in profil.items():
        seuil = int(seuil_str.strip(">="))
        if fiabilite >= seuil:
            mise = int(solde * pct)
            break
    else:
        mise = int(solde * profil.get("<60", 0.15))
    # conseils basés sur la part du solde
    part = mise / solde if solde else 0
    if part >= 0.50:
        conseil = "Fonce !"
    elif part >= 0.35:
        conseil = "Bonne chance, bon potentiel."
    elif part >= 0.20:
        conseil = "Risque modéré, mise réduite."
    else:
        conseil = "Très risqué, petite mise conseillée."
    return mise, conseil

def enregistrer_pari(data):
    with open(historique_fichier, "a") as f:
        f.write(data + "\n")

def bilan_final():
    try:
        with open(historique_fichier, "r") as f:
            lignes = f.readlines()
        total = len(lignes)
        gagnes = sum("GAGNÉ" in l for l in lignes)
        print("\n--- Bilan Final ---")
        print(f"Nombre de paris : {total}")
        print(f"Succès : {gagnes}")
        print(f"Échecs : {total - gagnes}")
    except FileNotFoundError:
        print("Aucun historique trouvé.")

# === Profils intelligents ===
def creer_profil_intelligent(nom):
    type_joueur = input("Quel type de joueur es-tu ? (Brutal, Prudent, etc.) : ").strip().lower()
    profil = {
        "brutal": {">=90": 0.25, ">=75": 0.20, ">=60": 0.15, "<60": 0.10},
        "prudent": {">=90": 0.15, ">=75": 0.10, ">=60": 0.05, "<60": 0.02}
    }
    return profil.get(type_joueur, {">=90": 0.20, ">=75": 0.15, ">=60": 0.10, "<60": 0.05})

# === MENU PRINCIPAL ===
if __name__ == "__main__":
    profils = charger_profils()
    bankroll = charger_bankroll()

    print("=== Bienvenue dans ton outil de prédiction FIFA 5x5 ===")

    while True:
        print("1. Créer un profil")
        print("2. Charger un profil")
        print("3. Consulter l'historique")
        print("4. Faire une prédiction")
        print("5. Quitter")
        choix = input("Que veux-tu faire ? (1/2/3/4/5) : ").strip()

        if choix == '1':
            nom = input("Nom du profil : ").strip()
            type_profil = input("Souhaitez-vous créer un profil intelligent ? (o/n) : ").strip().lower()
            if type_profil == 'o':
                profils["profils"][nom] = creer_profil_intelligent(nom)
            else:
                profils["profils"][nom] = {}
                for seuil in [90, 75, 60, 0]:
                    pct = float(input(f"Mise (%) pour fiabilité >= {seuil}% : "))
                    profils["profils"][nom][f">={seuil}"] = pct
            profils["profil_actif"] = nom
            sauvegarder_profils(profils)
            print(f"Profil '{nom}' créé et activé.")

        elif choix == '2':
            if not profils["profils"]:
                print("Aucun profil disponible. Crée-en un d'abord.")
            else:
                print("Profils disponibles :", ", ".join(profils["profils"].keys()))
                sel = input("Nom du profil à charger : ").strip()
                if sel in profils["profils"]:
                    profils["profil_actif"] = sel
                    sauvegarder_profils(profils)
                    print(f"Profil '{sel}' activé.")
                else:
                    print("Profil non trouvé.")

        elif choix == '3':
            bilan_final()

        elif choix == '4':
            actif = profils.get("profil_actif")
            if not actif:
                print("Aucun profil actif. Charge ou crée un profil d'abord.")
            else:
                solde = bankroll["capital_actuel"]
                continuer = True
                while continuer:
                    print("\n--- Nouvelle simulation ---")
                    dm = demande_scores("DOMICILE - Total buts")
                    d1 = demande_scores("DOMICILE - 1ère mi-temps")
                    em = demande_scores("EXTERIEUR - Total buts")
                    e1 = demande_scores("EXTERIEUR - 1ère mi-temps")

                    print("\nCalcul en cours...")
                    time.sleep(1)

                    moy1 = moyenne_ponderee(d1) + moyenne_ponderee(e1)
                    moym = moyenne_ponderee(dm) + moyenne_ponderee(em)
                    fiab = score_fiabilite(moy1, moym)

                    mise1, cons1 = suggere_mise(fiab, solde, actif, profils)
                    misem, consm = suggere_mise(fiab, solde, actif, profils)

                    print(f"\nMoy 1ère mi-temps : {moy1} | Moy match : {moym} | Fiabilité : {fiab}%")
                    print(f"Mise 1H : {mise1} F — {cons1}")
                    print(f"Mise match : {misem} F — {consm}")

                    # Suggestions de paris
                    if moy1 >= 1.5:
                        print("1. Over 1.5 en 1ère mi-temps conseillé")
                    elif moy1 >= 1:
                        print("1. Over 1.0 possible mais risqué")
                    else:
                        print("1. Moins de 1 but probable")
                    if moym >= 5:
                        print("2. Over 4.5 conseillé")
                    elif moym >= 3.5:
                        print("2. Over 3.5 possible")
                    else:
                        print("2. Match fermé probable")
                    if moyenne_ponderee(d1) >= 0.8 and moyenne_ponderee(e1) >= 0.8:
                        print("3. BTTS 1H conseillé")
                    else:
                        print("3. BTTS 1H risqué")

                    # Type de pari
                    print("\nSur quel pari as-tu joué ? 1) 1H  2) Match  3) Les deux")
                    tp = input("Choix (1/2/3) : ").strip()
                    types = {"1": "1ère mi-temps", "2": "Match entier", "3": "Les deux"}
                    pari = types.get(tp, "Non précisé")

                    # Demander la cote du pari
                    cote = float(input(f"Entrez la cote pour le pari ({pari}) : "))

                    # Résultat
                    res = input("Gagné ? (o/n) : ").strip().lower()
                    etat = "GAGNÉ" if res == 'o' else "PERDU"

                    # Entraînement local
                    equipes = f"{sum(dm)} - {sum(em)}"
                    entrainement_local(equipes, [sum(dm), sum(em)], fiab, etat, cote, pari)

                    # Suivi de bankroll
                    gain = misem if etat == "GAGNÉ" else 0
                    perte = misem if etat == "PERDU" else 0
                    suivre_bankroll(misem, gain, perte)

                    # Enregistrement dans l'historique texte
                    enregistrer_pari(f"Fiabilité: {fiab}% | Pari: {pari} | Cote: {cote} | Résultat: {etat}")

                    # Affichage du nouveau capital
                    cap = charger_bankroll()["capital_actuel"]
                    print(f"Capital actuel : {cap} F")

                    # Continuer ?
                    if input("Continuer ? (o/n) : ").strip().lower() != 'o':
                        continuer = False

        elif choix == '5':
            print("Au revoir !")
            break

        else:
            print("Option invalide, relance le programme.")
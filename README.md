# Predictor
Outil de Prédiction FIFA 5x5

Ce projet est un outil de prédiction pour les paris sportifs basé sur des statistiques de matchs FIFA 5x5. Il permet de suivre la bankroll, d’enregistrer l’historique des paris, de prédire des cotes en fonction des performances passées des équipes, et de suggérer des mises sur la base de profils de parieurs intelligents.

Il comprend également des fonctionnalités d’entraînement local pour améliorer les prédictions, ainsi que le suivi des résultats des paris.

Fonctionnalités

Gestion de profils de parieurs : Créez des profils personnalisés et intelligents pour définir des stratégies de mise.

Prédictions de paris : Prédisez les résultats en utilisant les performances passées des équipes.

Suivi de bankroll : Gérez votre capital et suivez vos gains et pertes.

Historique des paris : Gardez une trace de tous vos paris et de leurs résultats.

Calcul du critère de Kelly : Utilisez le critère de Kelly pour maximiser vos mises en fonction des probabilités.

Entraînement local : Améliorez les prédictions avec des données historiques.


Prérequis

Python 3.x

Modules Python nécessaires (disponibles via requirements.txt ou installation manuelle) :

time

json

os



Installation

1. Clonez le dépôt sur votre machine :

git clone https://github.com/hasprogamer/Predictor



2. Exécution du script : Lancez le programme en exécutant le fichier Python principal :

python votre_fichier.py



Utilisation

1. Création d'un profil : Lors du lancement du programme, vous pouvez choisir de créer un profil en sélectionnant l'option 1. Vous pouvez choisir entre un profil intelligent (préconfiguré avec des stratégies de mise) ou un profil personnalisé.


2. Charger un profil : Sélectionnez l'option 2 pour charger un profil déjà existant. Cela vous permettra de continuer avec les mêmes paramètres.


3. Consultation de l'historique des paris : Sélectionnez l'option 3 pour voir le bilan des paris précédents.


4. Faire une prédiction : Sélectionnez l'option 4 pour entrer les données des derniers matchs d'une équipe et obtenir des suggestions de paris.


5. Quitter : Sélectionnez l'option 5 pour quitter le programme.



Exemple de prédiction

Lors de l'utilisation de l'option 4, le programme vous demandera d'entrer les scores des 5 derniers matchs de chaque équipe. Ensuite, il calculera les moyennes pondérées des scores, la fiabilité de la prédiction, et suggérera des paris (par exemple, Over 1.5, BTTS, etc.) en fonction des résultats des matchs précédents.

Gestion de la bankroll

Le programme suit la bankroll (capital actuel) et ajuste la mise suggérée en fonction des résultats des paris précédents. Le critère de Kelly est utilisé pour déterminer la taille optimale des mises en fonction des probabilités et des cotes.

Historique des paris

Tous les paris et leurs résultats (gagnés ou perdus) sont enregistrés dans un fichier texte pour un suivi facile. Vous pouvez consulter cet historique pour analyser les performances passées et améliorer votre stratégie de paris.

Auteurs

Rayfoul le Requin Blanc (Développeur principal)

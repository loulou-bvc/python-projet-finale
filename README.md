# Projet Python - Analyse des Réservations Hôtelières

## 📋 Description

Ce projet effectue une analyse complète des données de réservations hôtelières. Il inclut le nettoyage des données, l'analyse statistique et la création de visualisations pour mieux comprendre les tendances et les comportements des clients.

## 🎯 Objectifs

- Nettoyer et préparer les données pour l'analyse
- Analyser les tendances de réservations
- Identifier les facteurs influençant les annulations
- Visualiser les données pour une meilleure compréhension
- Générer des statistiques clés sur les réservations

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Télécharger le dataset**
   
   - Lien: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
   - Téléchargez le fichier `hotel_bookings.csv`
   - Placez-le dans le dossier `data/` (créez le dossier si nécessaire)

## 🚀 Utilisation

### Exécuter l'analyse complète

```bash
python main.py
```

Le script va:
1. Charger les données depuis `data/hotel_bookings.csv`
2. Nettoyer et préparer les données
3. Effectuer l'analyse statistique
4. Générer les visualisations dans le dossier `output/`

### Structure du projet

```
python-projet-finale/
│
├── main.py                 # Script principal
├── data_cleaning.py        # Module de nettoyage des données
├── data_analysis.py        # Module d'analyse et visualisation
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation du projet
│
├── data/                  # Données (à télécharger depuis Kaggle)
│   └── hotel_bookings.csv
│
└── output/                # Résultats de l'analyse
    ├── 1_taux_annulation.png
    ├── 2_distribution_prix.png
    ├── 3_reservations_par_mois.png
    ├── 4_duree_sejour.png
    ├── 5_top_pays.png
    ├── 6_correlation_matrix.png
    └── 7_segment_marche.png
```

## 📊 Fonctionnalités

### Nettoyage des données
- Suppression des doublons
- Gestion des valeurs manquantes
- Conversion des types de données
- Calcul de nouvelles variables (durée de séjour, nombre de personnes, revenu total)
- Suppression des valeurs aberrantes

### Analyses effectuées
- Statistiques descriptives
- Taux d'annulation par type d'hôtel
- Analyse des prix moyens journaliers (ADR)
- Tendances saisonnières
- Analyse géographique (pays d'origine)
- Analyse des segments de marché
- Analyse de corrélation entre variables

### Visualisations générées
1. **Taux d'annulation par type d'hôtel** - Compare les taux d'annulation entre City Hotel et Resort Hotel
2. **Distribution des prix** - Histogramme montrant la distribution des prix moyens journaliers
3. **Réservations par mois** - Tendances saisonnières des réservations
4. **Durée de séjour moyenne** - Comparaison entre les types d'hôtels
5. **Top 10 pays** - Les pays d'origine les plus fréquents
6. **Matrice de corrélation** - Corrélations entre les variables numériques clés
7. **Segment de marché** - Répartition des réservations par segment

## 📈 Résultats attendus

Après exécution, vous obtiendrez:
- Des statistiques résumées dans la console
- 7 graphiques haute résolution sauvegardés dans `output/`
- Une meilleure compréhension des tendances de réservations

## 🛠️ Technologies utilisées

- **Python 3** - Langage de programmation
- **Pandas** - Manipulation et analyse de données
- **NumPy** - Calculs numériques
- **Matplotlib** - Visualisation de données
- **Seaborn** - Visualisations statistiques avancées

## 📝 Notes

- Les données doivent être placées dans le dossier `data/` avant l'exécution
- Le dossier `output/` sera créé automatiquement lors de l'exécution
- Les graphiques sont sauvegardés en format PNG haute résolution (300 DPI)

## 👤 Auteur

Projet réalisé dans le cadre d'un cours Python

## 📄 Licence

Ce projet est fourni à titre éducatif.


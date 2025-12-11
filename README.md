# Analyse Exploratoire de la Demande Hôtelière

## Description

Projet d'analyse exploratoire des données de réservations hôtelières comparant les **City Hotels** et **Resort Hotels**. 

**Projet :** 8PRO408 - Outils de programmation pour la science des données  
**Dataset :** Hotel Booking Demand (119,390 réservations, 32 variables)

## Colaborateurs
Loup
Frantxa Cabrejos, CAB016105000

## Objectifs

- Explorer la structure et la qualité des données
- Comparer les deux types d'hôtels sur plusieurs indicateurs
- Étudier les comportements de réservation (saisonnalité, durée, prix, annulation)
- Identifier les profils de clients et leurs comportements
- Produire des visualisations pertinentes (statistiques et interactives)
- Résumer les observations dans un rapport analytique

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Linux/macOS
   # venv\Scripts\activate   # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Télécharger le dataset**
   - Lien: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
   - Téléchargez le fichier `hotel_bookings.csv`
   - Placez-le dans le dossier `data/` (créez le dossier si nécessaire)

## Utilisation

### Option 1 : Notebook Jupyter (Analyse complète)

**Important :** Avant de lancer Jupyter, assurez-vous que toutes les dépendances sont installées :
```bash
pip install -r requirements.txt
```

Lancez Jupyter Notebook :
```bash
jupyter notebook
```

**Configuration du kernel :** Si vous obtenez une erreur `ModuleNotFoundError`, suivez ces étapes :

1. **Vérifiez votre environnement** :
   ```bash
   python3 check_environment.py
   ```

2. **Assurez-vous d'utiliser le bon kernel dans Jupyter** :
   - Dans Jupyter Notebook, cliquez sur "Kernel" → "Change Kernel"
   - Sélectionnez "Python 3.13 (Projet Finale)" (le kernel spécifique créé pour ce projet)
   - Ou utilisez le kernel Python par défaut qui pointe vers votre environnement Python 3.13

3. **Si le kernel n'apparaît pas**, créez-le :
   ```bash
   python3 -m ipykernel install --user --name=python-projet-finale --display-name="Python 3.13 (Projet Finale)"
   ```

4. **Redémarrez le kernel** si nécessaire : "Kernel" → "Restart Kernel"

Ouvrez le fichier `analyse_hotels.ipynb` et exécutez toutes les cellules. Le notebook contient :
1. Exploration du dataset
2. Comparaison City Hotel vs Resort Hotel
3. Analyse temporelle
4. Analyse des comportements clients
5. Visualisations obligatoires (Matplotlib/Seaborn et Plotly)
6. Synthèse des résultats

### Option 2 : Application Streamlit (Interface interactive)

**En local :**

Lancez l'application Streamlit :
```bash
streamlit run app.py
```
ou consulter directement depuis l'hergement en ligne via le lien : https://python-projet-finale-3wuhjiowc4ivrm9bjrg478.streamlit.app/

L'application offre :
- Filtres interactifs (type d'hôtel, année, mois)
- Statistiques dynamiques
- Visualisations Plotly interactives
- Sélection de graphiques à afficher

### Option 3 : Scripts Python (Analyse basique)

Exécutez l'analyse basique avec les scripts Python :
```bash
python3 main.py
```

### Génération du rapport PDF

Pour générer le rapport PDF de synthèse :
```bash
python3 generate_rapport.py
```

Le rapport sera sauvegardé dans `rapport.pdf`.

## Structure du projet

```
python-projet-finale/
│
├── analyse_hotels.ipynb      # Notebook Jupyter complet
├── app.py                    # Application Streamlit
├── main.py                   # Script principal (analyse basique)
├── data_cleaning.py          # Module de nettoyage des données
├── data_analysis.py          # Module d'analyse et visualisation
├── generate_rapport.py       # Script de génération du rapport PDF
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
│
├── data/                     # Données (à télécharger depuis Kaggle)
│   └── hotel_bookings.csv
│
├── output/                   # Résultats de l'analyse (graphiques PNG)
│   └── *.png
│
└── rapport.pdf               # Rapport PDF de synthèse (généré)
```

## Fonctionnalités

### Analyses effectuées

1. **Exploration du dataset**
   - Aperçu des colonnes, types, valeurs manquantes
   - Détection des doublons
   - Nettoyage minimal des données

2. **Comparaison City Hotel vs Resort Hotel**
   - Taux d'annulation
   - Prix moyen (ADR)
   - Durée des séjours (weekend/weeknights)
   - Répartition des types de clients

3. **Analyse temporelle**
   - Saisonnalité (mois, semaines)
   - Tendances 2015-2017
   - Lead time (délais entre réservation et arrivée)

4. **Analyse des comportements clients**
   - Nombre d'adultes/enfants/bébés
   - Demandes spéciales
   - Types de dépôts (deposit_type)
   - Agents et entreprises

5. **Visualisations**
   - Histogrammes / countplots / boxplots (Seaborn/Matplotlib)
   - Visualisations interactives (Plotly)
   - Graphiques comparatifs entre les deux hôtels

6. **Synthèse**
   - Résultats et tendances clés
   - Limites des données
   - Pistes pour modélisation future

## Technologies utilisées

- **Python 3** - Langage de programmation
- **Pandas** - Manipulation et analyse de données
- **NumPy** - Calculs numériques
- **Matplotlib** - Visualisation de données
- **Seaborn** - Visualisations statistiques avancées
- **Plotly** - Visualisations interactives
- **Streamlit** - Interface web interactive
- **Jupyter** - Notebooks interactifs
- **ReportLab** - Génération de PDF

## Livrables

- **Notebook Jupyter** (`analyse_hotels.ipynb`) - Analyse complète et propre
- **Rapport PDF** (`rapport.pdf`) - Synthèse 1-2 pages (à générer avec `generate_rapport.py`)
- **Application Streamlit** (`app.py`) - Visualisations interactives
- **README.md** - Documentation du projet

## Notes

- Les données doivent être placées dans le dossier `data/` avant l'exécution
- Le dossier `output/` sera créé automatiquement lors de l'exécution des scripts Python
- Les graphiques Plotly dans le notebook et l'app Streamlit sont interactifs
- Le rapport PDF peut être régénéré à tout moment avec `generate_rapport.py`

## Contact

**Chargé de Cours :** HN Doukaga, hndoukag@uqac.ca  
**Cours :** 8PRO408 - Outils de programmation pour la science des données

## Licence

Ce projet est fourni à titre éducatif dans le cadre d'un cours universitaire.

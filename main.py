"""
Analyse des données de réservations hôtelières
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

try:
    plt.style.use('seaborn-v0_8-darkgrid')
except OSError:
    plt.style.use('seaborn-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

from data_cleaning import clean_data
from data_analysis import analyze_data, visualize_data


def main():
    print("=" * 60)
    print("ANALYSE DES RÉSERVATIONS HÔTELIÈRES")
    print("=" * 60)
    print()
    
    print("📂 Étape 1: Chargement des données...")
    try:
        df = pd.read_csv('data/hotel_bookings.csv')
        print(f"✅ Données chargées avec succès: {df.shape[0]} lignes et {df.shape[1]} colonnes")
    except FileNotFoundError:
        print("❌ Erreur: Fichier de données non trouvé!")
        print("   Le fichier data/hotel_bookings.csv doit être présent dans le projet")
        return
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return
    
    print()
    
    print("🧹 Étape 2: Nettoyage des données...")
    df_clean = clean_data(df)
    print(f"✅ Données nettoyées: {df_clean.shape[0]} lignes restantes")
    print()
    
    print("📊 Étape 3: Analyse des données...")
    stats = analyze_data(df_clean)
    print("✅ Analyse terminée")
    print()
    
    print("📈 Étape 4: Création des visualisations...")
    visualize_data(df_clean)
    print("✅ Visualisations créées et sauvegardées dans le dossier 'output/'")
    print()
    
    print("=" * 60)
    print("ANALYSE TERMINÉE AVEC SUCCÈS!")
    print("=" * 60)
    print("\n📋 Résumé des statistiques principales:")
    print(f"   • Nombre total de réservations: {stats['total_bookings']:,}")
    print(f"   • Taux d'annulation: {stats['cancellation_rate']:.2%}")
    print(f"   • Prix moyen par nuit: ${stats['avg_price']:.2f}")
    print(f"   • Durée moyenne de séjour: {stats['avg_stay']:.1f} nuits")
    print(f"   • Nombre moyen d'adultes: {stats['avg_adults']:.1f}")


if __name__ == "__main__":
    main()


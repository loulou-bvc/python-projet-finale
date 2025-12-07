
import pandas as pd
import numpy as np


def clean_data(df):
    """Nettoie et prépare les données pour l'analyse"""
    print("   • Suppression des doublons...")
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"     {initial_rows - len(df)} doublons supprimés")
    
    print("   • Gestion des valeurs manquantes...")
    df['children'] = df['children'].fillna(0)
    df['country'] = df['country'].fillna('Unknown')
    df['agent'] = df['agent'].fillna(0).astype(int)
    df['company'] = df['company'].fillna(0).astype(int)
    
    print("   • Conversion des types de données...")
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
    
    categorical_cols = ['hotel', 'meal', 'country', 'market_segment', 
                       'distribution_channel', 'reserved_room_type', 
                       'assigned_room_type', 'deposit_type', 'customer_type',
                       'reservation_status']
    
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
    
    print("   • Calcul de nouvelles variables...")
    df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['total_people'] = df['adults'] + df['children'] + df['babies']
    df['total_revenue'] = df['adr'] * df['total_stay']
    
    print("   • Suppression des valeurs aberrantes...")
    initial_rows = len(df)
    df = df[df['adr'] >= 0]
    df = df[df['adr'] < 10000]
    df = df[df['total_people'] > 0]
    df = df[df['total_stay'] > 0]
    print(f"     {initial_rows - len(df)} lignes avec valeurs aberrantes supprimées")
    
    return df


def get_data_info(df):
    """Affiche les informations générales sur le dataset"""
    print("\nInformations sur le dataset:")
    print(f"  Forme: {df.shape[0]} lignes × {df.shape[1]} colonnes")
    print(f"  Mémoire utilisée: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\nColonnes du dataset:")
    for col in df.columns:
        print(f"  - {col}: {df[col].dtype}")
    
    print(f"\nValeurs manquantes:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        for col, count in missing[missing > 0].items():
            print(f"  - {col}: {count} ({count/len(df)*100:.2f}%)")
    else:
        print("  Aucune valeur manquante")


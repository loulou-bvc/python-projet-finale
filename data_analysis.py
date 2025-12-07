import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('output', exist_ok=True)


def analyze_data(df):
    """Calcule les statistiques principales"""
    stats = {}
    
    stats['total_bookings'] = len(df)
    stats['cancellation_rate'] = (df['is_canceled'] == 1).sum() / len(df)
    stats['avg_price'] = df['adr'].mean()
    stats['avg_stay'] = df['total_stay'].mean()
    stats['avg_adults'] = df['adults'].mean()
    stats['total_revenue'] = df['total_revenue'].sum()
    
    stats['city_hotel_bookings'] = len(df[df['hotel'] == 'City Hotel'])
    stats['resort_hotel_bookings'] = len(df[df['hotel'] == 'Resort Hotel'])
    
    df['arrival_month'] = pd.to_datetime(df['arrival_date_year'].astype(str) + 
                                         '-' + df['arrival_date_month'].astype(str) + 
                                         '-01')
    stats['busiest_month'] = df.groupby('arrival_month').size().idxmax().strftime('%B %Y')
    
    return stats


def visualize_data(df):
    """Génère tous les graphiques d'analyse"""
    plt.rcParams['figure.figsize'] = (12, 6)
    
    print("   • Graphique 1: Taux d'annulation...")
    fig, ax = plt.subplots(figsize=(10, 6))
    cancellation_by_hotel = df.groupby('hotel')['is_canceled'].mean() * 100
    cancellation_by_hotel.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c'])
    ax.set_title('Taux d\'annulation par type d\'hôtel', fontsize=16, fontweight='bold')
    ax.set_xlabel('Type d\'hôtel', fontsize=12)
    ax.set_ylabel('Taux d\'annulation (%)', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    for i, v in enumerate(cancellation_by_hotel):
        ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig('output/1_taux_annulation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   • Graphique 2: Distribution des prix...")
    fig, ax = plt.subplots(figsize=(12, 6))
    df[df['adr'] < 500]['adr'].hist(bins=50, ax=ax, color='#9b59b6', edgecolor='black')
    ax.set_title('Distribution des prix moyens journaliers (ADR)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Prix par nuit (€)', fontsize=12)
    ax.set_ylabel('Nombre de réservations', fontsize=12)
    ax.axvline(df['adr'].mean(), color='red', linestyle='--', linewidth=2, 
               label=f'Moyenne: {df["adr"].mean():.2f}€')
    ax.legend()
    plt.tight_layout()
    plt.savefig('output/2_distribution_prix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   • Graphique 3: Réservations par mois...")
    df['arrival_date_month_num'] = pd.to_datetime(df['arrival_date_month'], format='%B').dt.month
    bookings_by_month = df.groupby('arrival_date_month_num').size()
    month_names = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                   'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bookings_by_month.plot(kind='line', marker='o', ax=ax, color='#27ae60', linewidth=2, markersize=8)
    ax.set_title('Nombre de réservations par mois', fontsize=16, fontweight='bold')
    ax.set_xlabel('Mois', fontsize=12)
    ax.set_ylabel('Nombre de réservations', fontsize=12)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/3_reservations_par_mois.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   • Graphique 4: Durée de séjour...")
    fig, ax = plt.subplots(figsize=(10, 6))
    stay_by_hotel = df.groupby('hotel')['total_stay'].mean()
    stay_by_hotel.plot(kind='bar', ax=ax, color=['#f39c12', '#16a085'])
    ax.set_title('Durée moyenne de séjour par type d\'hôtel', fontsize=16, fontweight='bold')
    ax.set_xlabel('Type d\'hôtel', fontsize=12)
    ax.set_ylabel('Durée moyenne (nuits)', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    for i, v in enumerate(stay_by_hotel):
        ax.text(i, v + 0.1, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig('output/4_duree_sejour.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   • Graphique 5: Top 10 pays...")
    top_countries = df['country'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    top_countries.plot(kind='barh', ax=ax, color='#e67e22')
    ax.set_title('Top 10 des pays d\'origine des clients', fontsize=16, fontweight='bold')
    ax.set_xlabel('Nombre de réservations', fontsize=12)
    ax.set_ylabel('Pays', fontsize=12)
    plt.tight_layout()
    plt.savefig('output/5_top_pays.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   • Graphique 6: Matrice de corrélation...")
    numeric_cols = ['is_canceled', 'lead_time', 'arrival_date_year', 
                    'arrival_date_week_number', 'stays_in_weekend_nights',
                    'stays_in_week_nights', 'adults', 'children', 'babies',
                    'adr', 'required_car_parking_spaces', 'total_of_special_requests']
    
    correlation_df = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(correlation_df, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title('Matrice de corrélation entre les variables numériques', 
                 fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('output/6_correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   • Graphique 7: Segment de marché...")
    market_segment = df['market_segment'].value_counts()
    fig, ax = plt.subplots(figsize=(12, 6))
    market_segment.plot(kind='bar', ax=ax, color='#3498db')
    ax.set_title('Répartition des réservations par segment de marché', 
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Segment de marché', fontsize=12)
    ax.set_ylabel('Nombre de réservations', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig('output/7_segment_marche.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   Tous les graphiques ont été créés")


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Réservations Hôtelières",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Analyse Exploratoire de la Demande Hôtelière")
st.markdown("**City Hotel vs Resort Hotel**")
st.markdown("---")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('data/hotel_bookings.csv')
    
    # Nettoyage rapide
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean['children'] = df_clean['children'].fillna(0)
    df_clean['country'] = df_clean['country'].fillna('Unknown')
    df_clean['agent'] = df_clean['agent'].fillna(0).astype(int)
    df_clean['company'] = df_clean['company'].fillna(0).astype(int)
    df_clean['total_stay'] = df_clean['stays_in_weekend_nights'] + df_clean['stays_in_week_nights']
    df_clean['total_people'] = df_clean['adults'] + df_clean['children'] + df_clean['babies']
    df_clean = df_clean[df_clean['adr'] >= 0]
    df_clean = df_clean[df_clean['adr'] < 10000]
    df_clean = df_clean[df_clean['total_people'] > 0]
    df_clean = df_clean[df_clean['total_stay'] > 0]
    
    return df_clean

df = load_data()

st.sidebar.header("Filtres")

# Filtre par type d'hôtel
hotel_types = st.sidebar.multiselect(
    "Type d'hôtel",
    options=df['hotel'].unique(),
    default=df['hotel'].unique()
)

# Filtre par année
years = st.sidebar.multiselect(
    "Année",
    options=sorted(df['arrival_date_year'].unique()),
    default=sorted(df['arrival_date_year'].unique())
)

# Filtre par mois
months = st.sidebar.multiselect(
    "Mois",
    options=sorted(df['arrival_date_month'].unique()),
    default=sorted(df['arrival_date_month'].unique())
)

# Application des filtres
df_filtered = df[
    (df['hotel'].isin(hotel_types)) &
    (df['arrival_date_year'].isin(years)) &
    (df['arrival_date_month'].isin(months))
]

st.header("Statistiques Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Réservations", f"{len(df_filtered):,}")

with col2:
    cancellation_rate = (df_filtered['is_canceled'].mean() * 100)
    st.metric("Taux d'annulation", f"{cancellation_rate:.2f}%")

with col3:
    avg_adr = df_filtered['adr'].mean()
    st.metric("Prix moyen (ADR)", f"${avg_adr:.2f}")

with col4:
    avg_stay = df_filtered['total_stay'].mean()
    st.metric("Durée moyenne séjour", f"{avg_stay:.1f} nuits")

st.markdown("---")

st.sidebar.header("Visualisations")
visualizations = st.sidebar.multiselect(
    "Sélectionner les graphiques à afficher",
    options=[
        "Comparaison City vs Resort",
        "Évolution temporelle",
        "Distribution des prix",
        "Lead Time",
        "Types de clients",
        "Matrice de corrélation",
        "Top pays"
    ],
    default=[
        "Comparaison City vs Resort",
        "Évolution temporelle",
        "Distribution des prix"
    ]
)

if "Comparaison City vs Resort" in visualizations:
    st.header("Comparaison City Hotel vs Resort Hotel")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Taux d\'annulation', 'Prix moyen (ADR)', 
                        'Durée moyenne de séjour', 'Lead Time moyen'),
        specs=[[{"type": "bar"}, {"type": "box"}],
               [{"type": "bar"}, {"type": "box"}]]
    )
    
    # Taux d'annulation
    cancel_by_hotel = df_filtered.groupby('hotel')['is_canceled'].mean() * 100
    fig.add_trace(
        go.Bar(x=cancel_by_hotel.index, y=cancel_by_hotel.values,
               marker_color=['#3498db', '#e74c3c'], showlegend=False),
        row=1, col=1
    )
    
    # Prix (ADR)
    city_adr = df_filtered[df_filtered['hotel'] == 'City Hotel']['adr']
    resort_adr = df_filtered[df_filtered['hotel'] == 'Resort Hotel']['adr']
    if len(city_adr) > 0:
        fig.add_trace(go.Box(y=city_adr, name='City Hotel', marker_color='#3498db'), row=1, col=2)
    if len(resort_adr) > 0:
        fig.add_trace(go.Box(y=resort_adr, name='Resort Hotel', marker_color='#e74c3c'), row=1, col=2)
    
    # Durée de séjour
    stay_by_hotel = df_filtered.groupby('hotel')['total_stay'].mean()
    fig.add_trace(
        go.Bar(x=stay_by_hotel.index, y=stay_by_hotel.values,
               marker_color=['#3498db', '#e74c3c'], showlegend=False),
        row=2, col=1
    )
    
    # Lead Time
    city_lead = df_filtered[df_filtered['hotel'] == 'City Hotel']['lead_time']
    resort_lead = df_filtered[df_filtered['hotel'] == 'Resort Hotel']['lead_time']
    if len(city_lead) > 0:
        fig.add_trace(go.Box(y=city_lead, name='City Hotel', marker_color='#3498db', showlegend=False), row=2, col=2)
    if len(resort_lead) > 0:
        fig.add_trace(go.Box(y=resort_lead, name='Resort Hotel', marker_color='#e74c3c', showlegend=False), row=2, col=2)
    
    fig.update_layout(
        height=800,
        title_text="Comparaison complète City Hotel vs Resort Hotel",
        title_x=0.5,
        font=dict(size=12)
    )
    
    fig.update_xaxes(title_text="Type d'hôtel", row=1, col=1)
    fig.update_yaxes(title_text="Taux (%)", row=1, col=1)
    fig.update_yaxes(title_text="ADR", row=1, col=2)
    fig.update_xaxes(title_text="Type d'hôtel", row=2, col=1)
    fig.update_yaxes(title_text="Nuits", row=2, col=1)
    fig.update_yaxes(title_text="Jours", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

if "Évolution temporelle" in visualizations:
    st.header("Évolution Temporelle des Réservations")
    
    df_filtered['arrival_date_month_num'] = pd.to_datetime(df_filtered['arrival_date_month'], format='%B').dt.month
    df_monthly = df_filtered.groupby(['arrival_date_year', 'arrival_date_month_num', 'hotel']).size().reset_index(name='count')
    df_monthly['month_year'] = df_monthly['arrival_date_year'].astype(str) + '-' + df_monthly['arrival_date_month_num'].astype(str).str.zfill(2)
    df_monthly = df_monthly.sort_values(['arrival_date_year', 'arrival_date_month_num'])
    
    fig = px.line(
        df_monthly,
        x='month_year',
        y='count',
        color='hotel',
        color_discrete_map={'City Hotel': '#3498db', 'Resort Hotel': '#e74c3c'},
        labels={'count': 'Nombre de réservations', 'month_year': 'Mois', 'hotel': 'Type d\'hôtel'},
        title='Évolution temporelle des réservations par type d\'hôtel',
        markers=True
    )
    
    fig.update_layout(
        height=500,
        xaxis_tickangle=-45,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

if "Distribution des prix" in visualizations:
    st.header("Distribution des Prix (ADR)")
    
    df_price = df_filtered[df_filtered['adr'] < 500]
    fig = px.histogram(
        df_price,
        x='adr',
        nbins=50,
        color='hotel',
        color_discrete_map={'City Hotel': '#3498db', 'Resort Hotel': '#e74c3c'},
        labels={'adr': 'Prix moyen journalier (ADR)', 'count': 'Nombre de réservations'},
        title='Distribution des prix par type d\'hôtel',
        opacity=0.7,
        barmode='overlay'
    )
    fig.update_layout(height=500, font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

if "Lead Time" in visualizations:
    st.header("Analyse du Lead Time")
    
    fig = px.histogram(
        df_filtered,
        x='lead_time',
        color='hotel',
        nbins=50,
        color_discrete_map={'City Hotel': '#3498db', 'Resort Hotel': '#e74c3c'},
        labels={'lead_time': 'Lead Time (jours)', 'count': 'Nombre de réservations'},
        title='Distribution du Lead Time par type d\'hôtel',
        opacity=0.7,
        barmode='overlay'
    )
    fig.update_layout(height=500, font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

if "Types de clients" in visualizations:
    st.header("Répartition des Types de Clients")
    
    customer_type_counts = pd.crosstab(df_filtered['hotel'], df_filtered['customer_type'])
    fig = px.bar(
        customer_type_counts.reset_index(),
        x='hotel',
        y=customer_type_counts.columns.tolist(),
        barmode='group',
        color_discrete_sequence=['#3498db', '#e74c3c', '#f39c12', '#16a085'],
        labels={'value': 'Nombre de réservations', 'hotel': 'Type d\'hôtel'},
        title='Répartition des types de clients par type d\'hôtel'
    )
    fig.update_layout(height=500, font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

if "Matrice de corrélation" in visualizations:
    st.header("Matrice de Corrélation")
    
    numeric_cols = ['is_canceled', 'lead_time', 'arrival_date_year', 
                    'stays_in_weekend_nights', 'stays_in_week_nights', 
                    'adults', 'children', 'babies', 'adr', 
                    'required_car_parking_spaces', 'total_of_special_requests',
                    'total_stay', 'total_people']
    
    correlation_df = df_filtered[numeric_cols].corr()
    
    fig = px.imshow(
        correlation_df,
        labels=dict(color="Corrélation"),
        color_continuous_scale='RdBu',
        aspect="auto",
        title="Matrice de corrélation interactive (variables numériques)",
        text_auto=True
    )
    
    fig.update_layout(height=700, font=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

if "Top pays" in visualizations:
    st.header("Top 10 des Pays d'Origine")
    
    top_countries = df_filtered['country'].value_counts().head(10)
    fig = px.bar(
        x=top_countries.values,
        y=top_countries.index,
        orientation='h',
        labels={'x': 'Nombre de réservations', 'y': 'Pays'},
        title='Top 10 des pays d\'origine des clients',
        color=top_countries.values,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=500, font=dict(size=12), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

# Footer
st.markdown("---")
st.markdown("**Projet :** 8PRO408 - Outils de programmation pour la science des données")
st.markdown("**Dataset :** Hotel Booking Demand (Kaggle)")


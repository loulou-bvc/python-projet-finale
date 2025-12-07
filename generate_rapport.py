from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import pandas as pd
import os

def generate_rapport():
    # Charger les données pour les statistiques
    df = pd.read_csv('data/hotel_bookings.csv')
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
    
    # Calculer les statistiques
    total_bookings = len(df_clean)
    cancellation_rate = df_clean['is_canceled'].mean() * 100
    avg_adr = df_clean['adr'].mean()
    avg_stay = df_clean['total_stay'].mean()
    
    city_bookings = len(df_clean[df_clean['hotel'] == 'City Hotel'])
    resort_bookings = len(df_clean[df_clean['hotel'] == 'Resort Hotel'])
    city_cancel_rate = df_clean[df_clean['hotel'] == 'City Hotel']['is_canceled'].mean() * 100
    resort_cancel_rate = df_clean[df_clean['hotel'] == 'Resort Hotel']['is_canceled'].mean() * 100
    city_adr = df_clean[df_clean['hotel'] == 'City Hotel']['adr'].mean()
    resort_adr = df_clean[df_clean['hotel'] == 'Resort Hotel']['adr'].mean()
    
    # Créer le PDF
    filename = "rapport.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Style pour les sous-titres
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Style pour le texte
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Titre
    story.append(Paragraph("Analyse Exploratoire de la Demande Hôtelière", title_style))
    story.append(Paragraph("City Hotel vs Resort Hotel", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Informations du projet
    story.append(Paragraph("<b>Projet :</b> 8PRO408 - Outils de programmation pour la science des données", styles['Normal']))
    story.append(Paragraph("<b>Dataset :</b> Hotel Booking Demand (119,390 réservations, 32 variables)", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Résumé exécutif
    story.append(Paragraph("Résumé Exécutif", heading_style))
    story.append(Paragraph(
        f"Cette analyse exploratoire examine {total_bookings:,} réservations hôtelières après nettoyage des données, "
        f"comparant les City Hotels et Resort Hotels sur plusieurs dimensions clés. Les résultats montrent des différences "
        f"significatives en termes de taux d'annulation ({cancellation_rate:.2f}% globalement), de prix moyen (${avg_adr:.2f}), "
        f"et de comportements de réservation entre les deux types d'hôtels.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Résultats clés - Annulations
    story.append(Paragraph("Résultats Clés", heading_style))
    story.append(Paragraph("<b>1. Taux d'annulation</b>", styles['Heading3']))
    story.append(Paragraph(
        f"Le City Hotel présente un taux d'annulation de {city_cancel_rate:.2f}%, significativement plus élevé que le "
        f"Resort Hotel ({resort_cancel_rate:.2f}%). Cette différence suggère que les clients des hôtels de ville ont tendance "
        f"à annuler davantage, possiblement en raison d'une plus grande flexibilité dans leurs plans de voyage.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Prix (ADR)
    story.append(Paragraph("<b>2. Prix moyen (ADR)</b>", styles['Heading3']))
    story.append(Paragraph(
        f"Le Resort Hotel affiche un prix moyen journalier de ${resort_adr:.2f}, contre ${city_adr:.2f} pour le City Hotel. "
        f"Cette différence de prix reflète probablement les services et commodités supplémentaires offerts par les hôtels de villégiature.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Saisonnalité
    story.append(Paragraph("<b>3. Saisonnalité</b>", styles['Heading3']))
    story.append(Paragraph(
        "Les données révèlent des patterns saisonniers clairs. Les City Hotels montrent une demande plus constante tout au long "
        "de l'année, tandis que les Resort Hotels présentent des pics saisonniers plus marqués, particulièrement pendant les "
        "périodes estivales et les vacances.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Types de clients
    story.append(Paragraph("<b>4. Types de clients</b>", styles['Heading3']))
    story.append(Paragraph(
        f"L'analyse montre que les clients 'Transient' dominent dans les deux types d'hôtels. Le City Hotel compte {city_bookings:,} "
        f"réservations tandis que le Resort Hotel en compte {resort_bookings:,}, avec des profils de clients légèrement différents "
        "selon le type d'établissement.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Tableau de statistiques
    story.append(Paragraph("Statistiques Comparatives", heading_style))
    data = [
        ['Métrique', 'City Hotel', 'Resort Hotel', 'Global'],
        ['Nombre de réservations', f'{city_bookings:,}', f'{resort_bookings:,}', f'{total_bookings:,}'],
        ['Taux d\'annulation (%)', f'{city_cancel_rate:.2f}%', f'{resort_cancel_rate:.2f}%', f'{cancellation_rate:.2f}%'],
        ['Prix moyen (ADR)', f'${city_adr:.2f}', f'${resort_adr:.2f}', f'${avg_adr:.2f}'],
        ['Durée moyenne séjour', f'{df_clean[df_clean["hotel"]=="City Hotel"]["total_stay"].mean():.1f} nuits',
         f'{df_clean[df_clean["hotel"]=="Resort Hotel"]["total_stay"].mean():.1f} nuits', f'{avg_stay:.1f} nuits']
    ]
    
    table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Limites
    story.append(Paragraph("Limites des Données", heading_style))
    story.append(Paragraph(
        "1. <b>Période limitée :</b> Les données couvrent seulement 2015-2017, limitant l'analyse de tendances long terme.<br/>"
        "2. <b>Valeurs manquantes :</b> Certaines colonnes (country, agent, company) contiennent des valeurs manquantes nécessitant des imputations.<br/>"
        "3. <b>Données historiques :</b> Ces données sont passées et la situation actuelle peut différer significativement.<br/>"
        "4. <b>Contexte géographique :</b> Les codes pays ISO nécessitent une conversion pour une analyse géographique approfondie.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Pistes pour modélisation
    story.append(Paragraph("Pistes pour Modélisation Future", heading_style))
    story.append(Paragraph(
        "1. <b>Prédiction des annulations :</b> Développer un modèle de classification utilisant le lead time, type de dépôt, saison, etc.<br/>"
        "2. <b>Optimisation des prix :</b> Créer un modèle de régression pour optimiser les prix selon la demande saisonnière.<br/>"
        "3. <b>Segmentation des clients :</b> Appliquer des techniques de clustering pour identifier des profils de clients similaires.<br/>"
        "4. <b>Prévision de la demande :</b> Implémenter un modèle de série temporelle pour prévoir les réservations futures.<br/>"
        "5. <b>Pricing dynamique :</b> Développer un système de pricing adaptatif basé sur la demande en temps réel.",
        body_style
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # Conclusion
    story.append(Paragraph("Conclusion", heading_style))
    story.append(Paragraph(
        "Cette analyse exploratoire révèle des différences significatives entre les City Hotels et Resort Hotels en termes "
        "de comportements de réservation, tarification et taux d'annulation. Ces insights peuvent informer les stratégies de "
        "marketing, de pricing et de gestion de la capacité pour les deux types d'établissements.",
        body_style
    ))
    
    doc.build(story)
    print(f"Rapport PDF généré : {filename}")

if __name__ == "__main__":
    generate_rapport()


#!/usr/bin/env python3
"""
Script de vérification de l'environnement Python
Vérifie que toutes les dépendances sont installées correctement
"""

import sys

print("=" * 60)
print("VÉRIFICATION DE L'ENVIRONNEMENT")
print("=" * 60)
print(f"\nPython: {sys.executable}")
print(f"Version: {sys.version}\n")

required_packages = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'plotly': 'plotly',
    'streamlit': 'streamlit',
    'jupyter': 'jupyter',
    'notebook': 'notebook',
    'reportlab': 'reportlab',
    'ipykernel': 'ipykernel'
}

print("Vérification des packages requis:\n")
missing = []
installed = []

for package, import_name in required_packages.items():
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'version inconnue')
        print(f"  ✓ {package:15s} {version:15s}")
        installed.append(package)
    except ImportError:
        print(f"  ✗ {package:15s} NON INSTALLÉ")
        missing.append(package)

print("\n" + "=" * 60)
if missing:
    print(f"\nERREUR: {len(missing)} package(s) manquant(s): {', '.join(missing)}")
    print("\nPour installer les dépendances manquantes:")
    print("  pip install -r requirements.txt")
    print("\nOu installez manuellement:")
    for pkg in missing:
        print(f"  pip install {pkg}")
    sys.exit(1)
else:
    print(f"\n✓ Tous les packages sont installés ({len(installed)}/{len(required_packages)})")
    print("\nPour créer un kernel Jupyter pour ce projet:")
    print("  python3 -m ipykernel install --user --name=python-projet-finale")
    print("\nEnsuite, dans Jupyter Notebook:")
    print("  Kernel → Change Kernel → Python 3 (Projet Finale)")
    print("=" * 60)


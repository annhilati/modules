from setuptools import setup, find_packages

# Die README-Datei lesen und ihren Inhalt in long_description speichern
with open("README.md", 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='acemeta',  # Name des Pakets
    version='0.2.6',  # Version des Pakets
    author='Annhilati',  # Autor
    #author_email='your.email@example.com',  # E-Mail des Autors
    description='Library for typical workflows',  # Kurze Beschreibung
    long_description=description,  # Lange Beschreibung aus README.md
    long_description_content_type='text/markdown',  # Inhaltstyp der langen Beschreibung
    #url='https://github.com/yourusername/your-repo',  # URL des Projekts
    packages=find_packages(),  # Automatische Paketerkennung
    install_requires=[
        "requests"
    ]
)

from setuptools import setup, find_packages

# Die README-Datei lesen und ihren Inhalt in long_description speichern
with open("README.md", 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='workflows.py',
    version='0.0.0', 
    author='Annhilati',
    description='Library for typical workflows',
    long_description=description, 
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "requests"
    ]
)

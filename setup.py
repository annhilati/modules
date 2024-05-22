from setuptools import setup, find_packages

setup(
    name="acemeta",
    version="0.0",
    packages=find_packages(),
    install_requires=["datetime"],  # Hier können Abhängigkeiten aufgelistet werden
    author="Annhilati",
    #author_email="Ihre Email",
    #description="Eine kurze Beschreibung Ihres Pakets",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    #url="https://example.com/mypackage",  # URL zu Ihrem Projekt (optional)
)

def getfiletext(file) -> str:
    """
    Returns a text files content as a string

    #### Arguments:
        file (str): Path to file whose content is to be extracted

    #### Returns:
        str: The files content

    #### Raises:
        FileNotFoundError: If the file does not exist
    """
    try:
        with open(file, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Die Datei unter dem Pfad {file} wurde nicht gefunden.")
    except IOError as e:
        raise IOError(f"Ein Fehler beim Lesen der Datei ist aufgetreten: {e}")
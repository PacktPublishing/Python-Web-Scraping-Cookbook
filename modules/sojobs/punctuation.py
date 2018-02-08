def remove_punctuation(tokens):
    punctuation = [':', ',', '.', "``", "''", '(', ')', '-', '!', '#', '&', '/', '\\', ';', '?']
    return [token for token in tokens if token not in punctuation]
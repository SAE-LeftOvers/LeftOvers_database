
def CreateDictionnaryOutOfString(str_to_convert: str):
    output_dico = {}
    clean_str = CleanString(str_to_convert)
    list_str_to_convert = clean_str.split(" ")
    for word in list_str_to_convert:
        key = word.lower()
        if (key == ''):
            continue
        if (output_dico.get(key) == None):
            output_dico[key] = 1
        else:
            output_dico[key] += 1
    return output_dico

def CleanString(str_to_clean: str):
    char_to_replace_by_space = ['*', '-', '.', '\'', '"', '(', ')', '[', ']', '{', '}', '_', ';', ',', '?', '\n', '!', ':', '\\', '#', '~', '<br/>', '&']
    for char_to_replace in char_to_replace_by_space:
        str_to_clean = str_to_clean.replace(char_to_replace, ' ')
    return str_to_clean

def MergeDictionnary(io_dico, dico2):
    for word in dico2:
        if (io_dico.get(word) == None):
            io_dico[word] = 1
        else:
            io_dico[word] += dico2[word]
    return io_dico

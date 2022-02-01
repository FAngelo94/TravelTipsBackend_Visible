from dictionary.it import it
from dictionary.en import en

dictionary_complete = { "it": it, "en": en }

def dictionary(language, sentence):
    try:
        return dictionary_complete[language][sentence]
    except:
        return sentence
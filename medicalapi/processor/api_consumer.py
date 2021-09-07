import requests


SYNONYMS = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/synonyms/json'
INGREDIENTS = 'https://rxnav.nlm.nih.gov/REST/allconcepts.json?tty=IN'

COUNTRIES_URL = 'https://restcountries.eu/rest/v2/region/'
         
def getIngredients():
    r = requests.get(INGREDIENTS)
    return r

def getSynonyms(name):
    url = SYNONYMS % (name,)
    r = requests.get(url)
    return r

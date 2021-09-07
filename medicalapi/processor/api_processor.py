from .api_consumer import getIngredients, getSynonyms
from datetime import datetime
import hashlib
import json
import pandas as pd
import re
import logging
from hermetrics.levenshtein import Levenshtein
from MySQLdb import _mysql

lev = Levenshtein()
logging.getLogger().setLevel(logging.INFO)

# DATABASE PARAMETERS
HOST = 'localhost'
USER = 'root'
DBPASS = 'root'
DBNAME = 'test'

def createConnection():
    db =_mysql.connect(host=HOST,
        user=USER,
        passwd=DBPASS,
        db=DBNAME)
    return db

def cleanIdentifiers(values):
    cleanedValues = []
    for text in values:
        lista = [s for s in re.findall(r'\d\.?\d*', text)]
        lista_str = ''.join(lista)
        cleanedValues.append(lista_str)
    return cleanedValues

def cleanCompounds(values):
    cleanedValues = []
    for text in values:
        lista_str = re.sub(r"[^a-zA-Z0-9]"," ",text)
        cleanedValues.append(lista_str)
    return cleanedValues

def cleanTraslations(values):
    cleanedValues = []
    for text in values:
        try:
            index = text.index('[') #obtenemos la posición del carácter h
            value = text[0:index]
            cleanedValues.append(value)
        except:
            pass
    return cleanedValues

def cleanData(identifiers,compounds,translations,ingredients):
    for key,values in identifiers.items():
        identifiers[key] = cleanIdentifiers(values)

    for key,values in compounds.items():
        compounds[key] = cleanCompounds(values)

    for key,values in translations.items():
        translations[key] = getTranslations(values)

    for key,values in ingredients.items():
        ingredients[key] = cleanCompounds(values)

    return identifiers, compounds, translations, ingredients
    
def getLenWords(text):
    caracteres = list(text)
    num_l = 0
    for l in caracteres:
        num_l = num_l + 1 if re.match(r'[A-z]',l) else num_l 
    return num_l

def getLenNumbers(text):
    caracteres = list(text)
    num_l = 0
    for l in caracteres:
        num_l = num_l + 1 if re.match(r'[0-9]',l) else num_l 
    return num_l

def evalIdentifier(text):
    if (re.search(r' *[0-9]',text) and re.match(r'[A-z]',text) and
        getLenWords(text) < getLenNumbers(text) and not re.match(r'[\]\[\(\)]',text)):
        return True
    else:
        return False

def getIdentifiers(values):
    data = []
    for val in values:
        if evalIdentifier(val):
            data.append(val)
    return data

def evalCompounds(text):
    if (re.search(r' *[0-9]',text) and re.match(r'[A-z]',text) and 
        re.match(r'[\]\[\(\)]',text)):
        return True
    else:
        return False

def getCompounds(values):
    data = []
    for val in values:
        if evalCompounds(val):
            data.append(val)
    return data

def evalIngredient(name,text):
    if (lev.similarity(name,text) > 0.3):
        return True
    else:
        return False

def getIngredient(name,values):
    data = []
    for val in values:
        if evalIngredient(name,val):
            data.append(val)
    return data

def evalTranslations(text):
    if re.search(r'[\[]INN',text):
        return True
    else:
        return False

def getTranslations(values):
    data = []
    for val in values:
        if evalTranslations(val):
            data.append(val)
    return data

def classifyData(synonyms):
    indentifiers = {}
    compounds = {}
    translations = {}
    ingredients = {}
    for key,values in synonyms.items():
        indentifiers[key] = getIdentifiers(values)
        compounds[key] = getCompounds(values)
        translations[key] = getTranslations(values)
        ingredients[key] = getIngredient(key,values)
    return indentifiers, compounds, translations, ingredients

def getData():
    logging.info(' consuming API ingredients...') 
    response = getIngredients()
    json_data = json.loads(response.text)
    ingredients_list = json_data['minConceptGroup']['minConcept']
    total_ingredients = len(ingredients_list)
    logging.info(' finished consumption...')
    logging.info(' total ingredients: ' + str(len(ingredients_list)))    
    ingredients_list = json_data['minConceptGroup']['minConcept']
    date_start = str(datetime.now())
    index = 1
    synonyms = {}
    logging.info(' consuming synonyms of ingredients...')
    for line in ingredients_list:
        logging.info(' current ingredient: ' + str(index) + ' / ' + str(total_ingredients))
        response = getSynonyms(line['name'])
        synonyms[line['name']] = response
        index = index + 1
    print('start time:' + date_start)
    print('final time:' + str(datetime.now()))
    for key,value in  synonyms.items():
        if value.status_code == 200:
            vals = json.loads(value.text)['InformationList']['Information'][0]['Synonym']
        else:
            vals = []
        synonyms[key] = vals
        
    return synonyms

def getStringValues(dict_values,typeval):
    identifiers_to_insert = []
    for key,values in dict_values.items():
        for val in values:
            line = (key,typeval,val)
            identifiers_to_insert.append(line)
    num_lines = len(identifiers_to_insert)
    identifiers_char = ''
    for num,line in enumerate(identifiers_to_insert):
        identifiers_char += str(line) + (',' if (num_lines - 1) > num else '')
    return identifiers_char

def insertValues(connection,identifiers,compounds,translations, ingredients):
    identifiers_char = getStringValues(identifiers,'identifier')
    compounds_char = getStringValues(compounds,'compound')
    translations_char = getStringValues(translations,'translation')
    ingredients_char = getStringValues(ingredients,'ingredient')
    
    if identifiers_char != '':
        query = """ 
                INSERT INTO synonyms 
                    (ingredient,
                    sym_type,
                    sym_value)
                VALUES """ + identifiers_char
        connection.query(query)
    if compounds_char != '':
        query = """ 
                INSERT INTO synonyms 
                    (ingredient,
                    sym_type,
                    sym_value)
                VALUES """ + compounds_char
        connection.query(query)
    if translations_char != '':
        query = """ 
                INSERT INTO synonyms 
                    (ingredient,
                    sym_type,
                    sym_value)
                VALUES """ + translations_char
        connection.query(query)
    if ingredients_char != '':
        query = """ 
                INSERT INTO synonyms 
                    (ingredient,
                    sym_type,
                    sym_value)
                VALUES """ + ingredients_char
        connection.query(query)

def dataProcess(execute=False):
    if execute:
        data = getData()
        logging.info(' classifying data...')
        identifiers,compounds,translations,ingredients = classifyData(data)
        logging.info(' cleaning data...')
        identifiers,compounds,translations,ingredients = cleanData(identifiers,compounds,translations, ingredients)
        connection = createConnection()
        logging.info(' inserting data...')
        insertValues(connection, identifiers,compounds,translations, ingredients)
        logging.info(' finished process...')
    
dataProcess()
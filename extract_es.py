import spacy
import pandas as pd
import numpy as np
import unicodedata
from Levenshtein import distance #pip install python-Levenshtein
from google.cloud import translate_v2 as translate
import os
from dotenv import load_dotenv

def remove_accents(input_str):
    # Normalize characters to NFKD form which separates characters from their accents
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    # Filter out the characters that are not in the ASCII range, i.e., accents and special symbols
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalized_levenshtein(source, target):
    max_len = max(len(source), len(target))
    if max_len == 0:
        return 1.0  # If both strings are empty, they are fully similar
    return 1 - (distance(source, target) / max_len)

# Function to remove unwanted words
def remove_unwanted_words(text):
    # Words to filter out
    filter_out = ['yo', 'tu', 'usted', 'nosotros', 'vosotros', 'vos', 'ellos', 'ella', 'el']
    # Split the text into words
    words = text.split()
    # Filter words to exclude those in filter_out
    filtered_words = [word for word in words if word not in filter_out]
    # Join the words back into a string
    word = ' '.join(filtered_words)

    # if len(words) != len(filtered_words):
    #     print(text +' -> '+ word)
    
    return word

def spanishify(text):
    pre = text
    # No special accents
    text = text.replace('ff', 'f')
    text = text.replace('igli', 'illi')
    text = text.replace('egli', 'ej')
    text = text.replace('gn', 'n')
    text = text.replace('azio', 'acio')
    text = text.replace('uzio', 'ucio')
    text = text.replace('izio', 'icio')
    text = text.replace('vv', 'v')

    if text.endswith('bile'):
        text = text[:-4] + 'ble'
    if text.endswith('ale'):
        text = text[:-3] + 'al'
    if text.endswith('ele'):
        text = text[:-3] + 'el'
    if text.endswith('attamente'):
        text = text[-9] + 'actamente'
    if text.endswith('are'):
        text = text[:-3] + 'ar'
    if text.endswith('ere'):
        text = text[:-3] + 'er'
    if text.endswith('ire'):
        text = text[:-3] + 'ir'
    if text.endswith('ione'):
        text = text[:-4] + 'ion'
    if text.endswith('enza'):
        text = text[:-4] + 'encia'
    if pre != text:
        print(pre, text)
    return text


load_dotenv()  
if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set.")


if os.path.isfile('temp/spanish.csv'): 
    print('doc with spanish exists...')
    df = pd.read_csv('temp/spanish.csv')
    if 'spagnolo' not in df.columns:
        df = pd.read_csv('temp/filtered_list.csv')
    df['spagnolo'] = df['spagnolo'].str.lower()
else:
    print('creating doc with spanish')
    df = pd.read_csv('temp/filtered_list.csv')

    # LEMMATIZE SPANISH
    translate_client = translate.Client()  # Assumes environment variable is set for auth
    lemma = df['lemma'].to_list()
    total_entries = len(lemma)
    maximum_words_per_request = 128
    spagnolo_list = []
    index = 0
    new_index = 0
    while index < total_entries:
        new_index = index + maximum_words_per_request
        if new_index > total_entries:
            new_index = total_entries
        print(lemma[index : new_index])
        spagnolo = translate_client.translate(lemma[index : new_index], target_language='es', source_language='it')
        spagnolo_list.extend([trans['translatedText'] for trans in spagnolo])

        index = new_index

    df['spagnolo'] = spagnolo_list 
    df['spagnolo'] = df['spagnolo'].str.lower()
    df.to_csv("temp/spanish.csv", index = False)

df = df.drop(columns=['it_reverse'])

nlp = spacy.load('es_core_news_lg')

df['spagnolo'] = df['spagnolo'].apply(remove_unwanted_words)
df = df[df['spagnolo'].str.strip().astype(bool)] # remove rows with only unwanted words

df['lemma_es'] = df['spagnolo'].apply(lambda x: nlp(x)[0].lemma_)
df['pos_es'] = df['spagnolo'].apply(lambda x: nlp(x)[0].pos_)

# Create elimination table
df_elim = df.head(0)
df_elim.to_csv("temp/mutually_intelligible.csv", index = False)

# Remove accents
df['temp_nfkd_it'] = df['lemma'].apply(lambda x: remove_accents(x))
df['temp_nfkd_es'] = df['spagnolo'].apply(lambda x: remove_accents(x))

# ELIMINATE EXACT MATCHES
i_elim = (df.temp_nfkd_it.str.lower() == df.temp_nfkd_es.str.lower())
df[i_elim].to_csv("temp/same_es.csv", index=False)
df[i_elim].drop(columns=['temp_nfkd_it', 'temp_nfkd_es']).to_csv("temp/mutually_intelligible.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

# df['filtered_spagnolo'] = df['spagnolo'].apply(remove_unwanted_words)

# Spanification
df['it_spanishify'] = df['lemma'].apply(lambda x: spanishify(x))

# Levenshtein model for closeness
levenshtein_score = []
for i, x in enumerate(df['spagnolo']):
    levenshtein_score.append(normalized_levenshtein(str(df.iloc[i]['it_spanishify']), str(df.iloc[i]['spagnolo'])))
df['levenshtein'] = levenshtein_score

i_elim = df['levenshtein'] > 0.75
df[i_elim].to_csv("temp/elim_levenshtein.csv", index=False)
df[i_elim].drop(columns=['it_spanishify','temp_nfkd_it', 'temp_nfkd_es','levenshtein']).to_csv("temp/mutually_intelligible.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

# Remove temp columns
# df.drop(columns=['temp_nfkd_it','temp_nfkd_es'])

# SAVE
df = df.sort_values(by='levenshtein', ascending=False)
df.to_csv('result/processed_parole_italiane.csv', index = False)

df_elim = pd.read_csv('temp/mutually_intelligible.csv')
df_elim = df_elim.sort_values(by='rango')
df_elim.to_csv("temp/mutually_intelligible.csv", index=False)
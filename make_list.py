import spacy
import pandas as pd
from google.cloud import translate_v2 as translate
import os
from dotenv import load_dotenv

nlp = spacy.load('it_core_news_md')

# Load environment variables from .env file
load_dotenv()  
if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set.")

# LOAD RAW LIST
df = pd.read_csv('raw.csv')


## LEMMATIZATION
# Roots like "aiutare ci" are converted to "aiutare"
print("Lemmatizing...")
df['lemma'] = df['parola'].apply(lambda x: nlp(x)[0].lemma_)
print("Done lemmatizing.")

## Translate to ENGLISH AND SPANISH
translate_client = translate.Client()  # Assumes environment variable is set for auth
print('Translating...')

parole = df['parola'].tolist()
[len(i) for i in parole]
total_chars = sum(len(i) for i in parole)
total_entries = len(df)
maximum_words_per_request = 128

inglese_list = []
spagnolo_list = []
italiano_rev_list = []
index = 0
new_index = 0
while index < total_entries:
    new_index = index + maximum_words_per_request
    if new_index > total_entries:
        new_index = total_entries
    
    inglese = translate_client.translate(parole[index : new_index], target_language='en', source_language='it')
    inglese_trans = [trans['translatedText'] for trans in inglese]
    inglese_list.extend(inglese_trans)
    
    spagnolo = translate_client.translate(parole[index : new_index], target_language='es', source_language='it')
    spagnolo_list.extend([trans['translatedText'] for trans in spagnolo])

    italiano_rev = translate_client.translate(inglese_trans, target_language='it', source_language='en')
    italiano_rev_list.extend([trans['translatedText'] for trans in italiano_rev])

    index = new_index

df['inglese'] = inglese_list
df['spagnolo'] = spagnolo_list
df['it_reverse'] = italiano_rev_list

df.to_csv('parole_italiane.csv', index=False)

print("Done.")

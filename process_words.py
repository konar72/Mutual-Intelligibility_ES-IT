import spacy
import pandas as pd
from google.cloud import translate_v2 as translate
from spacy.glossary import GLOSSARY 
pos_dict = GLOSSARY

nlp = spacy.load('it_core_news_sm')
df = pd.read_csv('parole_italiane.csv')

# TO DO CREATE LISTS OF ELIMINATED WORDS

## LEMMATIZATION
# Roots like "aiutare ci" are converted to "aiutare"
df['lemma'] = df['parola'].apply(lambda x: nlp(x)[0].lemma_.split(' ',1)[0])
# Drop any duplicates
df = df.sort_values(by='rango').drop_duplicates(subset='lemma', keep='first')

## Translate to English and eliminate exact matches

## PARTS OF SPEECH
df['pos'] = df['parola'].apply(lambda x: nlp(x)[0].pos_)
df['pos_def'] = df['pos'].apply(lambda x: pos_dict.get(x,"N/A"))
df = df[df.pos != 'X']

# print(df_sorted.head(10))

# Proper nouns
# df_sorted.loc[df_sorted['pos'] == "PROPN"].to_csv("propn.csv", index=False)
df = df.sort_values(by='pos')
df.to_csv('result/processed_parole_italiane.csv', index=False)

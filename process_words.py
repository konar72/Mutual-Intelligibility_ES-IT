import spacy
import pandas as pd
from google.cloud import translate_v2 as translate
import os
from dotenv import load_dotenv
from translate import Translator
from spacy.glossary import GLOSSARY
from dotenv import load_dotenv
load_dotenv()
pos_dict = GLOSSARY
# Load environment variables from .env file
load_dotenv()  
if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set.")


nlp = spacy.load('it_core_news_md')
df = pd.read_csv('parole_italiane.csv')

# TODO CREATE LISTS OF ELIMINATED WORDS

df.drop(columns='frequenza',inplace=True)

# Eliminate the same lemmas
df['lemma'] = df['lemma'].apply(lambda x: x.split(' ',1)[0])
df = df.sort_values(by='rango').drop_duplicates(subset='lemma', keep='first')
print(len(df))

## PARTS OF SPEECH
df['pos'] = df['parola'].apply(lambda x: nlp(x)[0].pos_)
# df['pos_en'] = df['inglese'].apply(lambda x: nlp(x)[0].pos_)
# df['pos_def'] = df['pos'].apply(lambda x: pos_dict.get(x,"XX"))



# Treetagger
# Ensure the data types are consistent and appropriate
# df['it_reverse'] = df['it_reverse'].astype(str)
# df['inglese'] = df['inglese'].astype(str)

# # Lowercase transformation for comparison
# df['it_reverse_lower'] = df['it_reverse'].str.lower()
# df['inglese_lower'] = df['inglese'].str.lower()

# # Find matches and print them
# matches = df[df['it_reverse_lower'] == df['inglese_lower']]
# for index, row in matches.iterrows():
#     print('Match:', row['it_reverse'], row['inglese'])
#     df.at[index, 'parola'] = row['inglese']

# # Optional: Drop the temporary lowercase columns if no longer needed
# df.drop(columns=['it_reverse_lower', 'inglese_lower'], inplace=True)

# df['pos2'] = df['parola'].apply(lambda x: nlp(x)[0].pos_)

# Create elimination table
df_elim = df.head(0)
df_elim.to_csv("result/eliminated.csv", index = False)

# Eliminate entries that are symbols/undefined

# Keep words that are likely italian proper nouns
i_elim = (
    (df.pos == 'PROPN') & (
        (df.parola.str.lower() == df.inglese.str.lower()) & 
        (df.parola.str.lower() != df.it_reverse.str.lower())
    )
)
df_elim = df[i_elim].copy()
df_elim.to_csv("temp/elim_propn.csv", index = False)
df_elim.to_csv("result/eliminated.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

i_elim = (
    (df.parola.str.contains("'")) | 
    (df.pos == 'X') | 
    (df.pos == 'XX') | 
    (df.pos == 'SYM') | 
    (df.parola.str.len() < 2) & (df.lemma.str.len() < 2)
)
df_elim = df[i_elim].copy()
df_elim.to_csv("temp/elim_sym.csv", index = False)
df_elim.to_csv("result/eliminated.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

# Select words English
# TODO: problem here is that certain words like 
#   idea, computer, opera, radio, cinema, are lost. 
i_elim = (df.parola.str.lower() == df.inglese.str.lower())
df_elim = df[i_elim].copy()
df_elim.to_csv("temp/elim_en.csv", index=False)
df_elim.to_csv("result/eliminated.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

df_compare = df[df.parola == df.spagnolo]
df_compare.to_csv("temp/same_es.csv", index=False)

# Proper nouns
# df_sorted.loc[df_sorted['pos'] == "PROPN"].to_csv("propn.csv", index=False)
df = df.sort_values(by='rango')
df.to_csv('result/processed_parole_italiane.csv', index = False)

df_elim = pd.read_csv('result/eliminated.csv')
df_elim = df_elim.sort_values(by='rango')
df_elim.to_csv("result/eliminated.csv", index=False)

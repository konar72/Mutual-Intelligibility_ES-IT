import spacy
import pandas as pd

nlp = spacy.load('it_core_news_md')

df = pd.read_csv('parole_italiane.csv')
df.drop(columns='frequenza',inplace=True)

# ELIMINATE WORDS WITH SAME LEMMAS
# Words that are the same, just different conjugations or plural/singular, etc.
# This is by far the most impactful filter to reduce the list.
print('Removing repeated lemmas (total words: ' + str(len(df)) + ')...')
df['lemma'] = df['lemma'].apply(lambda x: x.split(' ',1)[0])
df = df.sort_values(by='rango').drop_duplicates(subset='lemma', keep='first')
print('Reduced list to: ' + str(len(df)) + ' words.')

## CREATE PARTS OF SPEECH
df['pos'] = df['parola'].apply(lambda x: nlp(x)[0].pos_)

# Create elimination table
df_elim = df.head(0)
df_elim.to_csv("temp/elim_all_filtered_list.csv", index = False)

# ELIMINATE ENGLISH PROPER NOUNS
i_elim = (
    (df.pos == 'PROPN') & (
        (df.parola.str.lower() == df.inglese.str.lower()) & 
        (df.parola.str.lower() != df.it_reverse.str.lower())
    )
)
df_elim = df[i_elim].copy()
df_elim.to_csv("temp/elim_propn.csv", index = False)
df_elim.to_csv("temp/elim_all_filtered_list.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

# ELIMINATE ENTRIES THAT ARE SYMBOLS, ABBREVIATIONS, OR UNDEFINED PARTS OF SPEECH
i_elim = (
    (df.parola.str.contains("'")) | 
    (df.pos == 'X') | 
    (df.pos == 'XX') | 
    (df.pos == 'SYM') | 
    (df.parola.str.len() < 2) & (df.lemma.str.len() < 2)
)
df_elim = df[i_elim].copy()
df_elim.to_csv("temp/elim_sym.csv", index = False)
df_elim.to_csv("temp/elim_all_filtered_list.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

# SELECT ALL ENGLISH WORDS
# TODO: problem here is that certain words like 
#   idea, computer, opera, radio, cinema, are lost. 
i_elim = (df.parola.str.lower() == df.inglese.str.lower())
df_elim = df[i_elim].copy()
df_elim.to_csv("temp/elim_en.csv", index=False)
df_elim.to_csv("temp/elim_all_filtered_list.csv", mode = 'a', index = False, header = False)

df = df[~i_elim]

# SAVE
df = df.sort_values(by='rango')
df.to_csv('temp/filtered_list.csv', index = False)

df_elim = pd.read_csv('temp/elim_all_filtered_list.csv')
df_elim = df_elim.sort_values(by='rango')
df_elim.to_csv("temp/elim_all_filtered_list.csv", index=False)

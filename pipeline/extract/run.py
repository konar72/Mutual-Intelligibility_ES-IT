"""Stage 3: Translate to Spanish, score all words for mutual intelligibility."""

import os
import sys
import pandas as pd
import nltk

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from translate_spanish import translate_to_spanish
from clean_spanish import clean_and_lemmatize
from score import score_all_words

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

load_dotenv()
if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set.")

# Load filtered list and translate to Spanish
df = pd.read_csv(os.path.join(ROOT, 'temp/filtered_list.csv'))
cache_path = os.path.join(ROOT, 'temp/spanish.csv')
df = translate_to_spanish(df, cache_path)

# Drop back-translation column (only needed in stage 2)
if 'it_reverse' in df.columns:
    df = df.drop(columns=['it_reverse'])

# Clean and lemmatize Spanish
df = clean_and_lemmatize(df)

# Score every word
df = score_all_words(df)

# Sort by score descending, then by rank
df = df.sort_values(by=['score', 'rango'], ascending=[False, True])

# Save
output_cols = ['rango', 'parola', 'lemma', 'inglese', 'pos', 'spagnolo', 'lemma_es', 'pos_es', 'match_type', 'score']
df[output_cols].to_csv(os.path.join(ROOT, 'output/all_words_scored.csv'), index=False)
print(f'\nWrote {len(df)} entries to output/all_words_scored.csv')

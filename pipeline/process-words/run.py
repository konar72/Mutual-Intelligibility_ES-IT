"""Stage 2: Filter the word list by removing duplicates, proper nouns, symbols, and English words."""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deduplicate import deduplicate_lemmas
from pos_tag import add_pos_tags
from filters import eliminate_proper_nouns, eliminate_symbols, eliminate_english_words

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

df = pd.read_csv(os.path.join(ROOT, 'input', '240510_Matthias-Buchmeier_Italian-frequency-list-1-5000.csv'))
df.drop(columns='frequenza', inplace=True)

df = deduplicate_lemmas(df)
df = add_pos_tags(df)

# Initialize elimination log
all_eliminated = df.head(0)

# Apply filters, logging each elimination
df, elim = eliminate_proper_nouns(df)
elim.to_csv(os.path.join(ROOT, "temp/elim_propn.csv"), index=False)
all_eliminated = pd.concat([all_eliminated, elim])

df, elim = eliminate_symbols(df)
elim.to_csv(os.path.join(ROOT, "temp/elim_sym.csv"), index=False)
all_eliminated = pd.concat([all_eliminated, elim])

df, elim = eliminate_english_words(df)
elim.to_csv(os.path.join(ROOT, "temp/elim_en.csv"), index=False)
all_eliminated = pd.concat([all_eliminated, elim])

# Save
df = df.sort_values(by='rango')
df.to_csv(os.path.join(ROOT, 'temp/filtered_list.csv'), index=False)

all_eliminated = all_eliminated.sort_values(by='rango')
all_eliminated.to_csv(os.path.join(ROOT, "temp/elim_all_filtered_list.csv"), index=False)

print(f'Filtered list: {len(df)} words. Eliminated: {len(all_eliminated)}.')

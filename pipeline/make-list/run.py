"""Stage 1: Load raw Italian word list, lemmatize, and translate."""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Allow imports from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lemmatize import lemmatize
from translate import translate_words

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

load_dotenv()
if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set.")

df = pd.read_csv(os.path.join(ROOT, 'input', '240510_Matthias-Buchmeier_Italian-frequency-list-1-5000.csv'),
                  usecols=['rango', 'parola', 'frequenza'])
df = lemmatize(df)
df = translate_words(df)
df.to_csv(os.path.join(ROOT, 'input', '240510_Matthias-Buchmeier_Italian-frequency-list-1-5000.csv'), index=False)

print("Done.")

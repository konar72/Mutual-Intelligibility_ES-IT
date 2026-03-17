"""Convert mutually_intelligible_pairs.csv to data.json for the GitHub Pages site."""

import csv
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'mutually_intelligible_pairs.csv')
JSON_PATH = os.path.join(SCRIPT_DIR, 'results_for_display.json')

KEEP_COLS = ['rango', 'parola', 'lemma', 'pos', 'spagnolo', 'lemma_es', 'levenshtein']

rows = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        entry = {}
        for col in KEEP_COLS:
            val = row[col]
            if col == 'rango':
                entry[col] = int(val)
            elif col == 'levenshtein':
                entry[col] = round(float(val), 3) if val else None
            else:
                entry[col] = val
        rows.append(entry)

rows.sort(key=lambda r: r['rango'])

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False)

print(f'Wrote {len(rows)} entries to {JSON_PATH}')

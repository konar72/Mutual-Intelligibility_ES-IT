"""Convert mutually_intelligible_pairs.csv to a JSON file for the GitHub Pages site.
Also updates the README title and description from config.json."""

import csv
import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'mutually_intelligible_pairs.csv')
JSON_PATH = os.path.join(SCRIPT_DIR, 'data.json')
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.json')
README_PATH = os.path.join(SCRIPT_DIR, '..', 'README.md')

# Load config
with open(CONFIG_PATH, encoding='utf-8') as f:
    config = json.load(f)

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

# Write data.json with config embedded
output = {'config': config, 'rows': rows}
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False)

print(f'Wrote {len(rows)} entries to {JSON_PATH}')

# Update README title and description
with open(README_PATH, encoding='utf-8') as f:
    readme = f.read()

full_title = config['title'] + ': ' + config['subtitle'] if config.get('subtitle') else config['title']
readme = re.sub(r'^# .+$', f'# {full_title}', readme, count=1, flags=re.MULTILINE)
# Replace the first paragraph after the title (the description line)
readme = re.sub(
    r'(^# .+\n\n).+?\n',
    rf'\1{config["description"]}\n',
    readme, count=1, flags=re.MULTILINE
)

with open(README_PATH, 'w', encoding='utf-8') as f:
    f.write(readme)

print(f'Updated README with title: {full_title}')

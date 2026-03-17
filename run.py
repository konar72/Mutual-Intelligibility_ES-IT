"""Run the full pipeline: make_list → process_words → extract_es → build site data."""

import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

steps = [
    ('Stage 1: Lemmatize and translate',   os.path.join(ROOT, 'pipeline', 'make-list', 'run.py')),
    ('Stage 2: Filter',                    os.path.join(ROOT, 'pipeline', 'process-words', 'run.py')),
    ('Stage 3: Score intelligibility',     os.path.join(ROOT, 'pipeline', 'extract', 'run.py')),
    ('Build site data',                    os.path.join(ROOT, 'docs', 'build_data.py')),
]

for label, script in steps:
    print(f'\n{"="*60}')
    print(f' {label}')
    print(f'{"="*60}\n')
    result = subprocess.run([sys.executable, script], cwd=ROOT)
    if result.returncode != 0:
        print(f'\nFailed at: {label}')
        sys.exit(result.returncode)

print(f'\n{"="*60}')
print(' Done.')
print(f'{"="*60}')

# Itañol 🇮🇹🤝🇪🇸
## Italian-Spanish Mutual Intelligibility: NLP Analysis of the 5,000 Most Common Italian Words 

Identifies which of the 5,000 most common Italian words are mutually intelligible with Spanish. The pipeline lemmatizes, translates, filters, and scores word pairs using a combination of exact matching, phonetic transformation rules, Levenshtein distance, and WordNet synonym expansion.

**Result:** 
~2,000 of the top 5,000 Italian words are mutually intelligible with Spanish. 

## Pipeline

The project runs as a three-stage pipeline. Each stage reads the previous stage's output.

### Stage 1: `make_list.py`

Processes the raw frequency list into a working dataset.

- **Input:** `raw.csv` (5,000 Italian words with rank and frequency, from [Matthias Buchmeier's Wiktionary list](https://en.m.wiktionary.org/wiki/User:Matthias_Buchmeier/Italian_frequency_list-1-5000))
- **Output:** `parole_italiane.csv`
- Lemmatizes Italian words using spaCy (`it_core_news_lg`)
- Translates each word to English via Google Cloud Translation API
- Back-translates English to Italian for validation
- Batches API requests in groups of 128

### Stage 2: `process_words.py`

Filters the word list down from ~5,000 to ~2,700 entries.

- **Input:** `parole_italiane.csv`
- **Output:** `temp/filtered_list.csv`
- Deduplicates words sharing the same lemma (keeps highest-frequency form)
- Removes proper nouns that translate identically to English
- Removes symbols, abbreviations, and single-character entries
- Removes words identical to their English translation (e.g., "computer")
- Adds part-of-speech tags
- Logs each elimination category to `temp/elim_*.csv`

**Known issue:** The English-word filter also removes legitimate Italian words that happen to be the same in English (e.g., *idea*, *opera*, *radio*, *cinema*). See the `TODO` in the code.

### Stage 3: `extract_es.py`

Determines mutual intelligibility between Italian and Spanish words.

- **Input:** `temp/filtered_list.csv`
- **Outputs:** `mutually_intelligible_pairs.csv`, `non_intelligible_pairs.csv`, `result/processed_parole_italiane.csv`

Three-pass matching strategy:

1. **Exact match** -- Italian and Spanish lemmas are identical after accent removal (e.g., *importante* / *importante*). ~244 pairs.
2. **Levenshtein after "spanishification"** -- Italian lemmas are transformed using phonetic rules (e.g., `-ione` to `-ion`, `ff` to `f`, `-bile` to `-ble`), then compared to Spanish. Pairs with normalized Levenshtein similarity > 0.75 are accepted. ~449 pairs.
3. **WordNet synonym expansion** -- For remaining words, Spanish synonyms are retrieved from NLTK WordNet. If any synonym has a normalized Levenshtein similarity >= 0.80 with the Italian lemma, the pair is accepted. ~1,300+ pairs.

## Spanishification Rules

Italian patterns are converted to their Spanish equivalents before comparison:

| Italian | Spanish | Example |
|---------|---------|---------|
| `ff` | `f` | *affetto* -> *afecto* |
| `igli` | `illi` | |
| `egli` | `ej` | |
| `gn` | `n` | *egnare* -> *enar* |
| `-azione` | `-acion` | *informazione* -> *informacion* |
| `-bile` | `-ble` | *possibile* -> *possible* |
| `-ale` | `-al` | *nazionale* -> *nacional* |
| `-are` | `-ar` | *parlare* -> *parlar* |
| `-ere` | `-er` | *sapere* -> *saper* |
| `-ire` | `-ir` | *partire* -> *partir* |
| `-ione` | `-ion` | *azione* -> *accion* |
| `-enza` | `-encia` | *differenza* -> *diferencia* |
| `vv` | `v` | |

## Setup

### Prerequisites

- Python 3.x
- Google Cloud Translation API credentials

### Installation

```bash
python3 -m venv venv
source venv/bin/activate

pip install spacy pandas numpy python-Levenshtein google-cloud-translate python-dotenv nltk

python -m spacy download it_core_news_lg
python -m spacy download es_core_news_lg
```

### Environment Variables

Create a `.env` file:

```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-cloud-credentials.json
```

### Running

```bash
python run.py                        # Run full pipeline + rebuild site data
```

Or run individual stages:

```bash
python pipeline/make-list/run.py    # Stage 1: lemmatize and translate
python pipeline/process-words/run.py # Stage 2: filter
python pipeline/extract/run.py      # Stage 3: score intelligibility
python docs/build_data.py           # Rebuild site data
```

## Project Structure

```
pipeline/                        # Processing scripts
  make-list/                     # Stage 1: lemmatize and translate
    lemmatize.py                 # Lemmatize Italian words with spaCy
    translate.py                 # Translate to English + back-translate
    run.py                       # Orchestrator
  process-words/                 # Stage 2: filter
    deduplicate.py               # Remove duplicate lemmas
    pos_tag.py                   # Add part-of-speech tags
    filters.py                   # Eliminate proper nouns, symbols, English words
    run.py                       # Orchestrator
  extract/                       # Stage 3: score intelligibility
    translate_spanish.py         # Translate to Spanish
    clean_spanish.py             # Clean and lemmatize Spanish
    spanishify.py                # Italian-to-Spanish phonetic rules
    similarity.py                # Levenshtein distance + WordNet synonyms
    score.py                     # Compute final intelligibility score
    run.py                       # Orchestrator
input/                           # Source and input data
  240510_Matthias-Buchmeier_Italian-frequency-list-1-5000.csv
                                 # 5,000 Italian words: lemmatized + translated
output/                          # Pipeline output
  all_words_scored.csv           # Final: all words with intelligibility scores
docs/                            # GitHub Pages site
  build_data.py                  # CSV to JSON converter
  index.html                     # Searchable word pair table
temp/                            # Intermediate files (gitignored)
```

## Data Source

[Italian frequency list (1-5000)](https://en.m.wiktionary.org/wiki/User:Matthias_Buchmeier/Italian_frequency_list-1-5000) by Matthias Buchmeier on Wiktionary.

## Changelog

| Date | Description |
|------|-------------|
| 2024-05-10 | Project started -- initial commit with raw word list and processing scripts |
| 2026-03-17 | Added more mutually intelligible pairs, WordNet integration |
| 2026-03-17 | Added comprehensive README |

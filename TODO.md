# TODO

## Bug Fixes
- [x] Fix truthy-tuple bug in `extract_es.py` — `is_mutually_intelligible()` returns a tuple which was always truthy
- [x] Fix `spanishify()` slice bug — `text[-9]` should be `text[:-9]`
- [x] Combine all three matching passes (exact, Levenshtein, WordNet) into `mutually_intelligible_pairs.csv` with a `match_type` column
- [ ] Fix English-word filter removing valid Italian words that happen to match English (e.g., *idea*, *opera*, *radio*, *cinema*) — consider an allowlist or spaCy-based validation

## Pipeline Improvements
- [ ] Use `nlp.pipe()` for batch processing instead of calling `nlp()` per row in `extract_es.py`
- [ ] Add more spanishification rules: `tt`->`t`, `pp`->`p`, `ss`->`s`, `zz`->`z`, `-ita`->`-idad`, `-aggio`->`-aje`
- [ ] Unify the three pipeline scripts into a single entry point or add a Makefile

## Website Features
- [ ] Three-tab view: Cognates, False Friends, Non-Cognates (requires fixing the tuple bug first for non-cognate data; false friends need a new detection pass)
- [ ] Transformation patterns page — group cognate pairs by which spanishification rule connects them so learners see patterns, not just word lists
- [ ] "You already know X%" stat — show what percentage of common Italian text a Spanish speaker can already comprehend
- [ ] Priority-ordered non-cognate study list — sorted by frequency rank so learners tackle the highest-impact unknown words first
- [X] Enable GitHub Pages deployment (Settings -> Pages -> source: main, folder: /docs)

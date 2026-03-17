# TODO

## Bug Fixes
- [ ] Fix truthy-tuple bug in `extract_es.py:192` — `is_mutually_intelligible()` returns a tuple which is always truthy, so all words end up in the intelligible list and `non_intelligible_pairs.csv` is always empty
- [ ] Fix `spanishify()` slice bug on line 86 — `text[-9]` should be `text[:-9]`
- [ ] Fix English-word filter removing valid Italian words that happen to match English (e.g., *idea*, *opera*, *radio*, *cinema*) — consider an allowlist or spaCy-based validation

## Pipeline Improvements
- [ ] Integrate `overrides.csv` — the file exists but is never loaded by any script
- [ ] Use `nlp.pipe()` for batch processing instead of calling `nlp()` per row in `extract_es.py`
- [ ] Add more spanishification rules: `tt`->`t`, `pp`->`p`, `ss`->`s`, `zz`->`z`, `-ita`->`-idad`, `-aggio`->`-aje`
- [ ] Unify the three pipeline scripts into a single entry point or add a Makefile

## Website Features
- [ ] Three-tab view: Cognates, False Friends, Non-Cognates (requires fixing the tuple bug first for non-cognate data; false friends need a new detection pass)
- [ ] Transformation patterns page — group cognate pairs by which spanishification rule connects them so learners see patterns, not just word lists
- [ ] "You already know X%" stat — show what percentage of common Italian text a Spanish speaker can already comprehend
- [ ] Priority-ordered non-cognate study list — sorted by frequency rank so learners tackle the highest-impact unknown words first
- [ ] Enable GitHub Pages deployment (Settings -> Pages -> source: main, folder: /docs)

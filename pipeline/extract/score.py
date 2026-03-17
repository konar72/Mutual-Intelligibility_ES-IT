"""Score every word for mutual intelligibility."""

import numpy as np
from similarity import remove_accents, normalized_levenshtein, best_synonym_score
from spanishify import spanishify


def score_all_words(df):
    """Add 'score' and 'match_type' columns to every word in the dataframe."""
    # Remove accents for comparison
    df['nfkd_it'] = df['lemma'].apply(remove_accents).str.lower()
    df['nfkd_es'] = df['spagnolo'].apply(remove_accents).str.lower()

    # Spanishify Italian lemmas
    df['it_spanishify'] = df['lemma'].apply(spanishify)

    # 1. Exact match after accent removal
    df['is_exact'] = df['nfkd_it'] == df['nfkd_es']

    # 2. Spanishified Levenshtein similarity
    df['lev_spanishify'] = df.apply(
        lambda r: normalized_levenshtein(str(r['it_spanishify']), str(r['spagnolo'])), axis=1
    )

    # 3. WordNet synonym score (skip exact and high-levenshtein words)
    print('Computing WordNet synonym scores...')
    df['lev_wordnet'] = 0.0
    needs_wordnet = ~df['is_exact'] & (df['lev_spanishify'] <= 0.75)
    for idx in df[needs_wordnet].index:
        s = best_synonym_score(df.at[idx, 'lemma'], df.at[idx, 'lemma_es'])
        df.at[idx, 'lev_wordnet'] = s
        if s > 0:
            print(f'  {df.at[idx, "lemma"]}: {df.at[idx, "lemma_es"]} -> {s:.3f}')

    # Final score: best of all methods
    df['score'] = np.where(
        df['is_exact'], 1.0,
        np.maximum(df['lev_spanishify'], df['lev_wordnet'])
    )

    # Match type label
    df['match_type'] = np.where(
        df['is_exact'], 'exact',
        np.where(
            df['lev_spanishify'] >= df['lev_wordnet'], 'levenshtein', 'wordnet'
        )
    )

    # Stats
    print(f'\nTotal words: {len(df)}')
    print(f'  Exact matches: {df["is_exact"].sum()}')
    print(f'  Score >= 0.75: {(df["score"] >= 0.75).sum()}')
    print(f'  Score >= 0.50: {(df["score"] >= 0.50).sum()}')
    print(f'  Score < 0.50:  {(df["score"] < 0.50).sum()}')

    return df

"""Filter functions that eliminate words from the list.

Each function returns (df_kept, df_eliminated).
"""

import os


def eliminate_proper_nouns(df):
    """Remove proper nouns that translate identically to English."""
    i_elim = (
        (df.pos == 'PROPN') & (
            (df.parola.str.lower() == df.inglese.str.lower()) &
            (df.parola.str.lower() != df.it_reverse.str.lower())
        )
    )
    return df[~i_elim], df[i_elim].copy()


def eliminate_symbols(df):
    """Remove symbols, abbreviations, and undefined parts of speech."""
    i_elim = (
        (df.parola.str.contains("'")) |
        (df.pos == 'X') |
        (df.pos == 'XX') |
        (df.pos == 'SYM') |
        (df.parola.str.len() < 2) & (df.lemma.str.len() < 2)
    )
    return df[~i_elim], df[i_elim].copy()


def eliminate_english_words(df):
    """Remove words identical to their English translation.

    TODO: This also removes valid Italian words that happen to match English
    (e.g., idea, computer, opera, radio, cinema).
    """
    i_elim = (df.parola.str.lower() == df.inglese.str.lower())
    return df[~i_elim], df[i_elim].copy()

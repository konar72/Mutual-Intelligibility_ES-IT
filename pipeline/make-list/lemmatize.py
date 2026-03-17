"""Lemmatize Italian words using spaCy."""

import spacy

nlp = spacy.load('it_core_news_lg')


def lemmatize(df):
    """Add a 'lemma' column with the base form of each word."""
    print("Lemmatizing...")
    df['lemma'] = df['parola'].apply(lambda x: nlp(x)[0].lemma_)
    print("Done lemmatizing.")

    print(df[df.isna().any(axis=1)])
    df = df.dropna()
    return df

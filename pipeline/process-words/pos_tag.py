"""Add part-of-speech tags using spaCy."""

import spacy

nlp = spacy.load('it_core_news_lg')


def add_pos_tags(df):
    df['pos'] = df['lemma'].apply(lambda x: nlp(x)[0].pos_)
    return df

"""Clean and lemmatize Spanish translations."""

import spacy

nlp = spacy.load('es_core_news_lg')

FILTER_OUT = {'yo', 'tu', 'tú', 'usted', 'nosotros', 'vosotros', 'vos', 'ellos', 'ella', 'el'}


def remove_unwanted_words(text):
    """Remove Spanish pronouns and articles from translated text."""
    words = text.split()
    filtered = [w for w in words if w not in FILTER_OUT]
    return ' '.join(filtered)


def clean_and_lemmatize(df):
    """Remove unwanted words, add Spanish lemma and POS columns."""
    df['spagnolo'] = df['spagnolo'].apply(remove_unwanted_words)
    df = df[df['spagnolo'].str.strip().astype(bool)]

    df['lemma_es'] = df['spagnolo'].apply(lambda x: nlp(x)[0].lemma_)
    df['pos_es'] = df['spagnolo'].apply(lambda x: nlp(x)[0].pos_)
    return df

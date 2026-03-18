import spacy
nlp = spacy.load('it_core_news_lg')


def lemmatize(df):
    """Add a 'lemma' column with the base form of each word."""
    
    print("Lemmatizing...")
    df['lemma'] = df['parola'].apply(lambda x: nlp(x)[0].lemma_)
    print("Done lemmatizing.") 

    # Fill any missing lemmas with the original word
    df['lemma'] = df['lemma'].fillna(df['parola'])

    return df

"""Remove words that share the same lemma, keeping the highest-frequency form."""


def deduplicate_lemmas(df):
    print('Removing repeated lemmas (total words: ' + str(len(df)) + ')...')
    df['lemma'] = df['lemma'].apply(lambda x: x.split(' ', 1)[0])
    df = df.sort_values(by='rango', ascending=True).drop_duplicates(subset='lemma', keep='first')
    df = df[df['lemma'].str.strip().astype(bool)]
    print('Reduced list to: ' + str(len(df)) + ' words.')
    return df

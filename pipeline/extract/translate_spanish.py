"""Translate Italian words to Spanish using Google Cloud Translation."""

import os
from google.cloud import translate_v2 as translate


def translate_to_spanish(df, cache_path, batch_size=128):
    """Add 'spagnolo' column. Uses cached file if available."""
    if os.path.isfile(cache_path):
        import pandas as pd
        print('Spanish translations cached, loading...')
        cached = pd.read_csv(cache_path)
        if 'spagnolo' in cached.columns:
            df = cached
            df['spagnolo'] = df['spagnolo'].str.lower()
            return df

    print('Translating to Spanish...')
    translate_client = translate.Client()
    parole = df['parola'].to_list()
    total = len(parole)
    spagnolo_list = []
    index = 0

    while index < total:
        end = min(index + batch_size, total)
        batch = parole[index:end]
        print(batch)
        result = translate_client.translate(batch, target_language='es', source_language='it')
        spagnolo_list.extend([t['translatedText'] for t in result])
        index = end

    df['spagnolo'] = spagnolo_list
    df['spagnolo'] = df['spagnolo'].str.lower()
    df.to_csv(cache_path, index=False)
    print('Done translating to Spanish.')
    return df

"""Translate Italian words to English and back-translate to Italian for validation."""

from google.cloud import translate_v2 as translate


def translate_words(df, batch_size=128):
    """Add 'inglese' (English) and 'it_reverse' (back-translated Italian) columns."""
    translate_client = translate.Client()
    print('Translating...')

    parole = df['parola'].tolist()
    total_entries = len(parole)

    inglese_list = []
    italiano_rev_list = []
    index = 0

    while index < total_entries:
        end = min(index + batch_size, total_entries)
        batch = parole[index:end]

        inglese = translate_client.translate(batch, target_language='en', source_language='it')
        inglese_trans = [t['translatedText'] for t in inglese]
        inglese_list.extend(inglese_trans)

        italiano_rev = translate_client.translate(inglese_trans, target_language='it', source_language='en')
        italiano_rev_list.extend([t['translatedText'] for t in italiano_rev])

        index = end

    df['inglese'] = inglese_list
    df['it_reverse'] = italiano_rev_list
    print('Done translating.')
    return df

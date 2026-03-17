"""String similarity functions using Levenshtein distance and WordNet synonyms."""

import unicodedata
from Levenshtein import distance
from nltk.corpus import wordnet as wn


def remove_accents(input_str):
    """Normalize to NFKD form and strip combining characters."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def normalized_levenshtein(source, target):
    """Return similarity score 0-1 (1 = identical)."""
    max_len = max(len(source), len(target))
    if max_len == 0:
        return 1.0
    return 1 - (distance(source, target) / max_len)


def get_synonyms(word, lang='ita'):
    """Get all WordNet synonyms for a word in a given language."""
    synsets = wn.synsets(word, lang=lang)
    synonyms = set()
    for synset in synsets:
        for lemma in synset.lemmas(lang=lang):
            synonyms.add(lemma.name())
    return synonyms


def best_synonym_score(lemma_ita, lemma_spa):
    """Return the best normalized Levenshtein score between the Italian lemma
    and all Spanish WordNet synonyms (including the lemma itself)."""
    synonyms_spa = get_synonyms(lemma_spa, lang='spa')
    synonyms_spa.add(lemma_spa)

    best = 0.0
    for syn_spa in synonyms_spa:
        nl = normalized_levenshtein(lemma_ita, syn_spa)
        if nl > best:
            best = nl
    return best

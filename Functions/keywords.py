''' Creation Date: 15/11/2022 '''

from keybert import KeyBERT


MODEL = KeyBERT(model = 'all-mpnet-base-v2')

# TODO: Hook keywords in, add user specified arguments.
def get_keywords(text: str):
    ''' Returns: List of keywords for given string. '''
    keywords = MODEL.extract_keywords(
        text,
        keyphrase_ngram_range = (1, 1),
        stop_words = 'english',
        highlight = False,
        top_n = 5
    )
    return list(dict(keywords).keys())


print(get_keywords('''The flexibility to apply regulatory approaches based on the risk'''))
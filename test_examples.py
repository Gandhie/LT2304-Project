import json
import random
from pprint import pprint

def load_from_json(filename):
    """Loads dictionary from json-file.

    Args:
        filename: a string which is the name of the file to load from.

    Returns:
        data: a dictionary representation of an XML-text, loaded from json-file.
    """
    if ".json" not in filename:
        filename = filename + ".json"

    with open(filename, encoding='utf-8') as input:
        data = json.load(input)

    print('Successfully loaded from file.')

    return data

def make_marked_sents(data):
    """Makes a list of paragraphs, where each paragraph is a list of sentences where
    determiners are marked with ** before and after, and nouns (if applicable) are marked
    with -- before and after.

    Args:
        data: a dictionary representation of an XML-text with "focus"-marking for determiners
        (and nouns, if this type of dictionary option is used).

    Returns:
        paras: a list of lists, where each list is a paragraph containing a list of sentences
        from the text, with determiners (and nouns if applicable) are marked.
    """
    paras = []
    for paragraph in data['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        sents = []
        if isinstance(sentence_lvl, dict):
            sent = []
            for word_meta in sentence_lvl['w']:
                if word_meta['focus'] == 1:
                    sent.append('**' + word_meta['word'] + '**')
                elif word_meta['focus'] == 2:
                    sent.append('--' + word_meta['word'] + '--')
                elif word_meta['focus'] == 0:
                    sent.append(word_meta['word'])
            sents.append(sent)
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                sent = []
                for word_meta in sentence['w']:
                    if word_meta['focus'] == 1:
                        sent.append('**' + word_meta['word'] + '**')
                    elif word_meta['focus'] == 2:
                        sent.append('--' + word_meta['word'] + '--')
                    elif word_meta['focus'] == 0:
                        sent.append(word_meta['word'])
                sents.append(sent)
        else:
            print("Found something that is not a dict/list!")
        paras.append(sents)

    return paras

def clean_sents(text):
    """Cleans the list of paragraphs so that each paragraph is a list of strings (sentences) instead of a list of lists (sentences).
    This function is only for showing the clean sentences with determiners (and nouns) marked up, and for use with the mini-game.

    Args:
        paras: a list of lists, where each contained list is a paragraph containing a list of sentences from the text, with determiners (and nouns if applicable) are marked.

    Returns:
        clean_paras: a list of lists of strings, where each contained list is a paragraph containing strings of sentences from the text, with determiners (and nouns if applicable) are marked.
    """
    paras = text.copy()
    clean_paras = []
    for para in paras:
        clean_para = []
        for sent in para:
            clean_sent = ''
            for word in sent[:(len(sent)-1)]:
                clean_sent += word + ' '
            for word in sent[(len(sent)-1):]:
                clean_sent += word
            clean_para.append(clean_sent)
        clean_paras.append(clean_para)

    return clean_paras

def mini_game(sentences):
    """Uses the list of cleaned up sentences to generate a few fill-in-the-blank questions as a proof-of-concept mini game.

    Args:
        sentences: a list of lists of strings, where each contained list is a paragraph containing strings of sentences from the text, with determiners (and nouns if applicable) are marked.

    Returns:
        -
    """
    all_sentences = []
    for para in sentences:
        for sent in para:
            all_sentences.append(sent)
    print(all_sentences)

if __name__ == "__main__":

    data_dt = load_from_json('marked-dt.json')
    data_dt_nn = load_from_json('marked-dt-nn')

    paras = make_marked_sents(data_dt_nn)
    #paras = make_marked_sents(data_dt)

    clean_paras = clean_sents(paras)

    mini_game(clean_paras)

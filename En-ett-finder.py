import xml.etree.ElementTree as ET
import json
from collections import defaultdict
from pprint import pprint
from copy import deepcopy

def make_text_dict(t):
    """Converts the XML-format parsed with ElementTree into a usable Python dictionary format which retains the structure.
    Used this recipe for direct XML-to-Dict conversion, credit to user K3---rnc:
    https://stackoverflow.com/a/10076823

    Args:
        t: The root element of the ElementTree tree.

    Returns:
        d: A Python dictionary representation of the XML-data."""
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(make_text_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['word'] = text
        else:
            d[t.tag] = text
    return d

def count_en_ett(text_dict):
    """Developing function, only used in development!
    Loops through a dictionary version of the XML-text and finds and counts all occurences of the determiners "en" and "ett" (also capitalised versions).
    Used to compare number of determiners found to manually counted determiners in the pdf-text.

    Args:
        text_dict: a dictionary representation of the XML-text.

    Returns:
        en: the count of "en" in the text.
        ett: the count of "ett" in the text."""
    en = 0
    ett = 0
    for paragraph in text_dict['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        if isinstance(sentence_lvl, dict):
            for word_meta in sentence_lvl['w']:
                if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                    en += 1
                elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                    ett += 1
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                for word_meta in sentence['w']:
                    if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                        en += 1
                    elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                        ett += 1
        else:
            print("Found something that is not a dict/list!")
    return en, ett

def count_dt_focus(marked_dict):
    """Developing function, only used during development!
    Counts the words (determiners) which has been marked as "focused" in the dictionary (specifically in the word metadata).
    Used to compare to the count found in count_en_ett().
    Also counts nouns marked as focused. Number will be 0 if nouns were not marked in the dictionary.

    Args:
        marked_dict: a dictionary representation of the XML-text, with the added word metadata attribute "focus".

    Returns:
        dt: the count of "focus"-marked words (determiners).
        nn: the count of "focus"-marked nouns (0 if nouns were not marked)."""
    dt = 0
    nn = 0
    for paragraph in marked_dict['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        if isinstance(sentence_lvl, dict):
            for word_meta in sentence_lvl['w']:
                if word_meta['focus'] == 1:
                    dt += 1
                elif word_meta['focus'] == 2:
                    nn += 1
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                for word_meta in sentence['w']:
                    if word_meta['focus'] == 1:
                        dt += 1
                    elif word_meta['focus'] == 2:
                        nn += 1
        else:
            print("Found something that is not a dict/list!")

    return dt, nn

def mark_all_dt(text_dict):
    """Loops through a dictionary representation of the XML-text and finds the determiners "en" and "ett" in the same way as count_en_ett().
    Adds an attribute "focus" to the metadata of all words and sets it to 1 if the word is an "en" or "ett" determiner, otherwise 0.
    This is the general approach which marks all "en" and "ett" determiners without looking at their nouns.

    Args:
        text_dict: a dictionary representation of the XML-text.

    Returns:
        marked_dict: a dictionary representation of the XML-text, with the added word metadata attribute "focus"."""
    marked_dict = deepcopy(text_dict)
    for paragraph in marked_dict['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        if isinstance(sentence_lvl, dict):
            for word_meta in sentence_lvl['w']:
                if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                    word_meta['focus'] = 1
                elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                    word_meta['focus'] = 1
                else:
                    word_meta['focus'] = 0
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                for word_meta in sentence['w']:
                    if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                        word_meta['focus'] = 1
                    elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                        word_meta['focus'] = 1
                    else:
                        word_meta['focus'] = 0
        else:
            print("Found something that is not a dict/list!")

    return marked_dict

def mark_dts_nn(marked_dict):
    """Loops through a dictionary representation of the XML-text where determiners have been "focus"-marked.
    Finds the "focus"-marked determiners and looks for their nouns from the words after the determiner until the end of the current sentence. The found noun is then marked with "focus": 2. Once the first noun of the right type for the determiner is found, it stops looking and moved on to the next determiner.
    This is an add-on to make the second approach of marking both determiners and their nouns possible.

    Args:
        marked_dict: a dictionary representation of the XML-text, with the added word metadata attribute "focus" (only determiners marked).

    Returns:
        nn_marked_dict: a dictionary representation of the XML-text, with the added wordmetadata attribute "focus" for both determiners (1) and their nouns (2)."""
    nn_marked_dict = deepcopy(marked_dict)
    for paragraph in nn_marked_dict['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        if isinstance(sentence_lvl, dict):
            for word_meta in sentence_lvl['w']:
                if word_meta['focus'] == 1:
                    start = sentence_lvl['w'].index(word_meta)
                    for noun_meta in sentence_lvl['w'][start:]:
                        if noun_meta['msd'] == 'NN.NEU.SIN.IND.NOM' or noun_meta['msd'] == 'NN.UTR.SIN.IND.NOM' or noun_meta['msd'] == 'NN.UTR.SIN.IND.GEN':
                            noun_meta['focus'] = 2
                            break
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                for word_meta in sentence['w']:
                    if word_meta['focus'] == 1:
                        start = sentence['w'].index(word_meta)
                        for noun_meta in sentence['w'][start:]:
                            if noun_meta['msd'] == 'NN.NEU.SIN.IND.NOM' or noun_meta['msd'] == 'NN.UTR.SIN.IND.NOM' or noun_meta['msd'] == 'NN.UTR.SIN.IND.GEN':
                                noun_meta['focus'] = 2
                                break
        else:
            print("Found something that is not a dict/list!")
    return nn_marked_dict

def save_to_json(marked_dict, filename):
    """Saves the dictionary representation with the "focus" attribute to a json-file.
    Make sure that you save the right type of dictionary, depending on if you want only determiners "focus"-marked or both determiners and their nouns.

    Args:
        marked_dict: a dictionary representation of the XML-text, with the added word metadata attribute "focus" for both determiners (1) and their nouns (2).
        filename: a string which will become the name of the file.
    Returns:
        -
    """
    if ".json" not in filename:
        filename = filename + ".json"

    with open(filename, 'w', encoding='utf-8') as output:
        json.dump(marked_dict, output, indent=4, ensure_ascii=False)

    print('Successfully saved to file.')

if __name__ == "__main__":
    '''Read XML-text from file. Change path to parse another XML-text.'''
    tree = ET.parse("F:\\Users\\Amelie\\Desktop\\B1_idrott\\C1_Skrivtrappan_Platsansokan.xml")
    root = tree.getroot()

    '''Makes dictionary representation of XML-text.'''
    text_dict = make_text_dict(root)
    '''Counts "en" and "ett".'''
    en, ett = count_en_ett(text_dict)
    #print(en, ett, (en+ett)) # Test print
    '''Adds focus attribute to word metadata and sets "en" and "ett" determiners to 1.'''
    dt_marked_dict = mark_all_dt(text_dict)
    #pprint(marked_dict) # Test print
    '''Counts focus-marked words (determiners).'''
    dt, nn = count_dt_focus(dt_marked_dict)
    #print('DT:', dt, '\nNN:', nn)  # Test print
    '''Adds focus attribute to word metadata for the nouns of the determiners (focus: 2).'''
    nn_marked_dict = mark_dts_nn(dt_marked_dict)
    #pprint(nn_marked_dict) # Test print
    '''Counts focus-marked words (determiners and nouns).'''
    dt2, nn2 = count_dt_focus(nn_marked_dict)
    #print('DT:', dt2, '\nNN:', nn2)  # Test print
    '''Saves marked dictionary to json-file (both versions of the dictionary here).'''
    save_to_json(dt_marked_dict, 'marked-dt')
    save_to_json(nn_marked_dict, 'marked-dt-nn.json')

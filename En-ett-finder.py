import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint

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
                    #print(word_meta['word'])
                    en += 1
                elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                    #print(word_meta['word'])
                    ett += 1
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                for word_meta in sentence['w']:
                    if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                        #print(word_meta['word'])
                        en += 1
                    elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                        #print(word_meta['word'])
                        ett += 1
        else:
            print("Found something that is not a dict/list!")
    return en, ett

def count_dt_focus(marked_dict):
    """Developing function, only used during development!
    Counts the words (determiners) which has been marked as "focused" in the dictionary (specifically in the word metadata).
    Used to compare to the count found in count_en_ett().

    Args:
        marked_dict: a dictionary representation of the XML-text, with the added word metadata attribute "focus".

    Returns:
        dt: the count of "focus"-marked words (determiners)."""
    dt = 0
    for paragraph in marked_dict['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        if isinstance(sentence_lvl, dict):
            for word_meta in sentence_lvl['w']:
                if word_meta['focus'] == 1:
                    #print(word_meta['word'])
                    dt += 1
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                for word_meta in sentence['w']:
                    if word_meta['focus'] == 1:
                        #print(word_meta['word'])
                        dt += 1
        else:
            print("Found something that is not a dict/list!")

    return dt

def mark_all_dt(text_dict):
    """Loops through a dictionary representation of the XML-text and finds the determiners "en" and "ett" in the same way as count_en_ett().
    Adds an attribute "focus" to the metadata of all words and sets it to 1 if the word is an "en" or "ett" determiner, otherwise 0.
    This is the general approach which marks all "en" and "ett" determiners without looking at their nouns.

    Args:
        text_dict: a dictionary representation of the XML-text.

    Returns:
        marked_dict: a dictionary representation of the XML-text, with the added word metadata attribute "focus"."""
    marked_dict = text_dict
    for paragraph in marked_dict['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        if isinstance(sentence_lvl, dict):
            for word_meta in sentence_lvl['w']:
                if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                    #print(word_meta['word'])
                    word_meta['focus'] = 1
                elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                    #print(word_meta['word'])
                    word_meta['focus'] = 1
                else:
                    word_meta['focus'] = 0
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                for word_meta in sentence['w']:
                    if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                        #print(word_meta['word'])
                        word_meta['focus'] = 1
                    elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                        #print(word_meta['word'])
                        word_meta['focus'] = 1
                    else:
                        word_meta['focus'] = 0
        else:
            print("Found something that is not a dict/list!")

    return marked_dict

# Read XML-text from file.
tree = ET.parse("F:\\Users\\Amelie\\Desktop\\B1_idrott\\B1_Rivstart_Idrott.xml")
root = tree.getroot()

# Makes dictionary representation of XML-text.
text_dict = make_text_dict(root)
# Counts "en" and "ett".
en, ett = count_en_ett(text_dict)
#print(en, ett, (en+ett)) # Test print
# Adds focus attribute to word metadata and sets "en" and "ett" determiners to 1.
marked_dict = mark_all_dt(text_dict)
#pprint(marked_dict) # Test print
# Counts focus-marked words (determiners).
dt = count_dt_focus(marked_dict)
#print(dt)  # Test print

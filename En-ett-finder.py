import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint

tree = ET.parse("F:\\Users\\Amelie\\Desktop\\B1_idrott\\B1_Rivstart_Idrott.xml")
root = tree.getroot()

"""Used this recipe for direct XML-to-Dict conversion, credit to user K3---rnc: https://stackoverflow.com/a/10076823"""
def make_text_dict(t):
    """"""
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
    """"""
    en = 0
    ett = 0
    for paragraph in text_dict['corpus']['text']['lessontext']['paragraph']:
        sentence_lvl = paragraph['sentence']
        #pprint(sentence_lvl)
        if isinstance(sentence_lvl, dict):
            #pprint(sentence_lvl['w'])
            for word_meta in sentence_lvl['w']:
                if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                    print(word_meta['word'])
                    en += 1
                elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                    print(word_meta['word'])
                    ett += 1
        elif isinstance(sentence_lvl, list):
            for sentence in sentence_lvl:
                #pprint(sentence['w'])
                for word_meta in sentence['w']:
                    if word_meta['msd'] == 'DT.UTR.SIN.IND' and (word_meta['word'] == 'en' or word_meta['word'] == 'En'):
                        print(word_meta['word'])
                        en += 1
                    elif word_meta['msd'] == 'DT.NEU.SIN.IND' and (word_meta['word'] == 'ett' or word_meta['word'] == 'Ett'):
                        print(word_meta['word'])
                        ett += 1
        else:
            print("Found something that is not a dict/list!")
    return en, ett


text_dict = make_text_dict(root)
en, ett = count_en_ett(text_dict)
print(en, ett)
#pprint(text_dict)

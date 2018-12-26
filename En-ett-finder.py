import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pprint

tree = ET.parse("F:\\Users\\Amelie\\Desktop\\B1_idrott\\B1_Rivstart_Idrott2.xml")
root = tree.getroot()

"""Used this recipe for direct XML-to-Dict conversion, credit to user K3---rnc: https://stackoverflow.com/a/10076823"""
def make_text_dict(t):
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

dict = make_text_dict(root)
pprint(dict)

# Getting the words in the dict (a dictionary with key w and a list of dictionaries of each word and its attributes (1 word = 1 dict in the list).). With full texts, this will probably need to be done on paragraph level and then iterating through sentences and words from there.
words = dict['corpus']['text']['lessontext']['paragraph']['sentence']

# Testing is done on B1_Idrott (the first sample text I got). Might wanna test for another 1-2 random texts for quality checking the algorithm later.
# This text contains (according to manual counting):
# 10x "en"
# 5x "ett"

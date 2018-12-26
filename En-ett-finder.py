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

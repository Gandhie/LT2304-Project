# LT2304-Project - Swedish Determiner Finder and Exercise Generator

This is a project for the LT2304 Language Technology Resources course of the MLT Programme at the University of Gothenburg.
The project is a script to find and mark Swedish determiners "en" and "ett" as well as their nouns in texts from textbooks for learning Swedish as a second language and, in a second script, generating some simple example exercises using these marked determiners and nouns.

## Script 1: En-ett-finder.py

__Running the script:__
```bash
python En-ett-finder.py
```

__Description:__
This script loads data from XML-files and converts them to a convenient Python dictionary format which roughly mirrors the XML-structure. It can then perform a sequence of operations to mark determiners and nouns in the dictionary by adding an additional attribute to word metadata called "focus".
Determiners = focus: 1
Nouns = focus: 2 (if applied, otherwise treated like other words)
Other words = focus: 0.
Once this attribute has been added to all words with the correct number, the dictionaries (the script creates one dictionary with marked nouns and one with unmarked nouns in its original form) are then saved as json-files for later use.

## Script 2: test_examples.py

__Running the script:__
```bash
python test_examples.py
```

__Description:__
This script loads the dictionaries from the saved json-files and then proceeds to reorganise the data into a list of paragraph lists, containing sentence lists of words. In these lists, determiners are surrounded by double ** and nouns (if applied) are surrounded by double --. These lists are then further cleaned up until the list is a simple list of strings, where each string is a full sentence. This last cleanup is done to facilitate the proof-of-concept mini game.
From the list of strings, the mini game function then picks a random sentence, makes sure that it contains a determiner by looking for the double ** , replaces the determiner with a blank slot and presents this as a fill-in-the-blank exercise to the user. The user can then input an answer which is checked against the actual determiner to give a response of correct/incorrect to the user depending on their answer. The script runs this minigame three times.


*Made by: Amelie Åstbom.*

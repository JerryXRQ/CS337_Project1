import data

import pandas as pd
import numpy as np
import re
import json
import matplotlib.pyplot as plt
from collections import defaultdict

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
import sys

# nltk pos reference (from Greeksforgeeks):
# CC coordinating conjunction
# CD cardinal digit
# DT determiner
# EX existential there (like: “there is” … think of it like “there exists”)
# FW foreign word
# IN preposition/subordinating conjunction
# JJ adjective ‘big’
# JJR adjective, comparative ‘bigger’
# JJS adjective, superlative ‘biggest’
# LS list marker 1)
# MD modal could, will
# NN noun, singular ‘desk’
# NNS noun plural ‘desks’
# NNP proper noun, singular ‘Harrison’
# NNPS proper noun, plural ‘Americans’
# PDT predeterminer ‘all the kids’
# POS possessive ending parent‘s
# PRP personal pronoun I, he, she
# PRP$ possessive pronoun my, his, hers
# RB adverb very, silently,
# RBR adverb, comparative better
# RBS adverb, superlative best
# RP particle give up
# TO to go ‘to‘ the store.
# UH interjection errrrrrrrm
# VB verb, base form take
# VBD verb, past tense took
# VBG verb, gerund/present participle taking
# VBN verb, past participle taken
# VBP verb, sing. present, non-3d take
# VBZ verb, 3rd person sing. present takes
# WDT wh-determiner which
# WP wh-pronoun who, what
# WP$ possessive wh-pronoun whose
# WRB wh-abverb where, when

invalid_1 = ['amy', 'jodie', 'tina', 'goldenglobes', 'married', 'fey']
invalid_2 = ['someone', 'globes', 'goldenglobes', 'poehler', 'foster', 'fey', 'home', 'j', 'taylor', 'shes', 'join',
             'way', 'tina', 'home']

# the one in nominee with minor modification
def find_person(tweets):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    filter = set(["golden globe", "the golden globe", "good", "goldenglobes", "series", "you", "tv", "awards",
                  "comedy", "season", "deserve", "award", "drama", "motion", "picture", "movie", "song", "great", "win"
                , "who", "what", "the", "guy", "tune", "nbc", "est", "askglobes", "ball", "madmen", "miniseriestv",
                  "someone","u","impresssiveeee","hell","dick",'kinda'])
    strict = set(["miniseriestv","oscar","congrats","goldengiobes","yay","lets"])
    for sentence in tweets:
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text not in filter:
                det=True
                for ele in strict:
                    if ele in ent.text:
                        det=False
                if "golden" in ent.text or "globe" in ent.text:
                    det=False
                if det:
                    res=ent.text.replace("best actress ","")
                    res = res.replace("hope ","")
                    res = res.replace(" best actress", "")
                    res = res.replace("best actor ", "")
                    res = res.replace(" best actor", "")
                    res = res.replace(" wins", "")
                    res = res.replace(" won","")
                    dic[res] += 1
    return dic


def main():
    possible = set(["2013", "2015", "2018", "2019"])
    year = '2013'
    if len(sys.argv) > 1 and sys.argv[1] in possible:
        year = str(sys.argv[1])
    # data initialization
    c = data.container(year)
    tweets = [" ".join(c.get(ele).text) for ele in c.keys()]
    people = find_person(tweets)
    names = [name for name in people.keys()]
    names.sort(key=lambda x: people[x], reverse=True)
    stp = set(stopwords.words('english'))
    num_person = 3
    num_first = 3

    # part of speech recognition for tweets subset of each person
    for i in range(num_person):
        name = names[i]

        # subset = [" ".join(c.get(ele).text) for ele in c.keys() if name in " ".join(c.get(ele).text)]
        subset = []
        for ele in c.keys():
            tweet = " ".join(c.get(ele).text)
            if name in tweet:
                subset.append(tweet)

        part_of_speech_word, part_of_speech_pos = [], []
        for tweet in subset:
            text_tokenized = word_tokenize(tweet)
            text_tokenized = [w for w in text_tokenized if not w in stp]
            values = nltk.pos_tag(text_tokenized)
            for word, pos in values:
                part_of_speech_word.append(word)
                part_of_speech_pos.append(pos)

        occurrences = {}
        for j, w in enumerate(part_of_speech_word):
            word, pos = w.lower(), part_of_speech_pos[j]
            if pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                index = j + 1
                while index < len(part_of_speech_word) and part_of_speech_pos[index] not in ['NN', 'NNS', 'NNP', 'NNPS']:
                    index += 1
                if index >= len(part_of_speech_word):
                    break
                noun = part_of_speech_word[index].lower()
                combined = word + ' ' + noun
                if combined not in occurrences.keys():
                    occurrences[combined] = 1
                else:
                    occurrences[combined] += 1

        combinations = [x for x in occurrences.keys()]
        combinations.sort(key=lambda x: occurrences[x], reverse=True)
        j, target = 0, num_first
        result = []
        while j < target and j < len(combinations):
            w1, w2 = combinations[j].split(" ")
            if w1 not in invalid_1 and w2 not in invalid_2:
                result.append(combinations[j])
            else:
                target += 1
            j += 1

        print(name, result)


if __name__ == '__main__':
    main()
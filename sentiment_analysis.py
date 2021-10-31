from soupsieve import select
import data
import spacy
import pandas as pd
import numpy as np
from collections import defaultdict
import nltk
import util
import winner
import re
from nltk.corpus import stopwords
from imdb import IMDb 
import multiprocessing
import winner
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

def sentiment(container, name):
    person_tweets = []
    sia = SentimentIntensityAnalyzer()
    for i in container.keys():
        m = container.get(i)
        lis = m.get_text()
        s = " ".join(lis)
        if name in s:
            person_tweets.append(s)
    sent = 0
    for i in person_tweets:
        sent += sia.polarity_scores(i)["compound"]
    sent = sent / len(person_tweets)
    #print(sent)

    return sent


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here

    c = data.container("2013")
    par = sentiment(c, "ben affleck")
    print(c)

if __name__ == '__main__':
    main()
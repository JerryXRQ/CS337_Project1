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

def party_hosts(container, year):
    key_word = set(["afterparty", "after party"])
    party_tweets = []
    for ele in container.keys():
        m = container.get(ele)
        lis=m.get_text()
        user = m.get_user()
        #print(user)
        s = " ".join(lis)
        for kw in key_word:
            if kw in s:
                party_tweets.append([lis, user, m.get_hashtags()])

    #party_tweets = np.unique(party_tweets).tolist()
    hosts = []
    for i in party_tweets:
        if "golden globes after party" in " ".join(i[0]):
            for j in range(len(i[0])):
                if i[0][j] == "golden":
                    if j >= 1:
                        hosts.append(i[0][j-1])
    remove = [year, "the", "at", "a", "on", "to", "official"]
    for i in remove:
        if i in hosts:
            hosts.remove(i)
    hosts = np.unique(hosts).tolist()
    print(hosts)
    return hosts


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here

    c = data.container("2015")
    par = party_hosts(c, "2015")
    #print(c)

if __name__ == '__main__':
    main()
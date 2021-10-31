'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util
import sys

def find_tweets(container):
    filter=set(["lol","joke","jokes","laugh","funny","humorous","humor"])
    res=[]
    counter=defaultdict(int)
    mes=defaultdict(list)

    nlp = spacy.load("en_core_web_sm")

    for keys in container.keys():
        message=container.get(keys)
        det=False
        for words in message.get_text():
            if words in filter:
                det=True
                break
        if det:
            res.append(message.get_text())
    potential=[]
    for ele in res:
        for i in range(len(ele)):
            if ele[i]=="joke":
                potential.append(ele[max(i-5,0):i])
    target=defaultdict(int)
    for i in range(2,5):
        for ele in potential:
            if len(ele)>=i:
                group=" ".join(ele[len(ele)-i:])
                target[group]+=1
    best=0
    choice=""
    for key in target.keys():
        if len(key.split())*target[key]>best:
            best=len(key)*target[key]
            choice=key
    print("Most Mentioned Joke Subject: ",choice)
    for ele in res:
        doc=nlp(" ".join(ele))
        for ent in doc.ents:
            if ent.label_=="PERSON":
                counter[ent.text]+=1
                mes[ent.text].append(ele)
    person=[e for e in counter.keys()]
    person.sort(key=lambda x:counter[x],reverse=True)
    print("People who made good jokes: ",person[:min(3,len(person))])

    return counter,mes







def main():
    possible=set(["2013","2015","2018","2019"])
    year='2013'
    if len(sys.argv)>1 and sys.argv[1] in possible:
        year=str(sys.argv[1])
    c=data.container(year)
    counter,message=find_tweets(c)
    key=[k for k in counter.keys()]
    key.sort(key=lambda x:counter[x],reverse=True)

    #print("Done")

if __name__ == '__main__':
    main()

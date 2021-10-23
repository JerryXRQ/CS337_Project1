'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util


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
    print(choice)
    for ele in res:
        doc=nlp(" ".join(ele))
        for ent in doc.ents:
            if ent.label_=="PERSON":
                counter[ent.text]+=1
                mes[ent.text].append(ele)


    return counter,mes







def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    c=data.container('2013')
    counter,message=find_tweets(c)
    key=[k for k in counter.keys()]
    key.sort(key=lambda x:counter[x],reverse=True)

    #print("Done")

if __name__ == '__main__':
    main()

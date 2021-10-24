'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util
from textblob import TextBlob


def red_carpet(container):
    filter=set(["golden","globes","golden globes","goldenglobes","redcarpetman"])
    res=[]
    counter=defaultdict(int)
    mes=defaultdict(float)

    nlp = spacy.load("en_core_web_sm")

    for keys in container.keys():
        message=container.get(keys)
        det=False
        sentence=" ".join(message.get_text())
        sentence+=" ".join(message.get_hashtags())
        if "red carpet" in sentence or "redcarpet" in sentence or "dress" in sentence:
            res.append(message.get_text())

    for ele in res:
        blob=TextBlob(" ".join(ele))
        #print(" ".join(ele))
        score=0
        if len(blob.sentences)>0:
            score=blob.sentences[0].sentiment.polarity
        doc=nlp(" ".join(ele))
        for ent in doc.ents:
            if ent.label_=="PERSON" and ent.text not in filter:
                res=ent.text
                res = res.replace(" goldenglobes", "")
                res = res.replace(" golden globes", "")
                res=res.replace(" wearing","")
                res=res.replace(" wears","")
                res=res.replace(" wear","")
                counter[res]+=1
                mes[res]+=score
    sentiment=[k for k in mes.keys()]
    mention=[k for k in counter.keys()]
    sentiment.sort(key=lambda x:mes[x],reverse=True)
    mention.sort(key=lambda y:counter[y],reverse=True)
    best=[]
    i=0
    while i<len(sentiment) and len(best)<3:
        if counter[sentiment[i]]>30:
            best.append(sentiment[i])
        i+=1
    worst=[]
    j = len(sentiment)-1
    while j>0 and len(worst) < 3:
        if counter[sentiment[j]] > 30:
            worst.append(sentiment[j])
        j -= 1
    print("Most Mentioned: ",mention[:min(len(mention),3)])
    print("Best Dressed: ", best)
    print("Worst Dressed: ", worst)


    return counter,mes







def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    c=data.container('2013')
    red_carpet(c)

    #print("Done")

if __name__ == '__main__':
    main()

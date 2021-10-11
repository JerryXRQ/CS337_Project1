'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util

def find_presenter(container,award):
    nlp = spacy.load("en_core_web_sm")
    candidate=defaultdict(int)
    reduce=util.process_name(award)
    #print(reduce)
    key_word=set(["present","presented","presents","presenting"])
    male_names = nltk.corpus.names.words('male.txt')
    female_names = nltk.corpus.names.words('female.txt')
    n=set(male_names+female_names)
    selected=[]
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        s=set(lis)
        det1=True
        det2=False
        for words in reduce:
            if words not in s:
                det1=False
                break
        if not det1:
            continue
        for kw in key_word:
            if kw in s:
                det2=True
        if det2:
            selected.append(lis)
    dic=defaultdict(int)
    for tweets in selected:
        sentence=""
        print(tweets)
        for i in range(len(tweets)):
            if tweets[i] in key_word:
                if i+1<len(tweets) and tweets[i+1]=="by":
                    sentence=" ".join(tweets[i+2:])
                else:
                    sentence=" ".join(tweets[:i])
        doc=nlp(sentence)
        for ent in doc.ents:
            if ent.label_=="PERSON":
                dic[ent.text]+=1
                #print(ent.text)
    k=[k for k in dic.keys()]
    k.sort(key=lambda x:dic[x],reverse=True)
    #print(k)
    for j in range(min(2,len(k))):
       print(k[j])
    #print(candidate)
    return





def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    file="gg2013.json"
    input=pd.read_json(file)
    c=data.container(input)
    find_presenter(c, "best performance by an actress in a motion picture - drama")
    print("Done")

if __name__ == '__main__':
    main()

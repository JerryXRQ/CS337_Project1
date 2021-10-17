'''Version 0.35'''
import pandas as pd
import data
import spacy
from collections import defaultdict
def find_host(container):
    host = set(["host", "hosts", "hosting", "hosted"])
    nlp = spacy.load("en_core_web_sm")
    selected=[]
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        for words in lis:
            if words in host:
                selected.append(' '.join(lis))
                break

    #Select the tweets that contain host keyword
    names=[]
    for tweet in selected:
        doc=nlp(tweet)
        for entity in doc.ents:
            if entity.label_=="PERSON":
                names.append(entity.text)
    #Use spacy to find the person labels
    dic=defaultdict(int)
    for n in names:
        dic[n]+=1
    keys=[k for k in dic.keys()]
    keys.sort(key=lambda x:dic[x],reverse=True)
    keys=keys[:5]
    reduced=[]
    for i in range(len(keys)):
        det=True
        for j in range(len(keys)):
            if i==j:
                continue
            else:
                if keys[i] in keys[j]:
                    det=False
                    break
        if det:
            reduced.append(keys[i])
    #Combine keys
    new=defaultdict(int)
    res=[]
    for ele in selected:
        for j in range(1,len(reduced)):
            if reduced[0] in ele and reduced[j] in ele:
                new[reduced[j]]+=1
    temp=reduced[1:]
    temp.sort(key=lambda x:new[x],reverse=True)
    res=[reduced[0],temp[0]]
    #Cross check the result to get the right answer
    #print(res,new)
    return res





def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    c=data.container("2015")
    find_host(c)

    print("success")

if __name__ == '__main__':
    main()

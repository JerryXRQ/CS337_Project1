'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict

def find_host(container):
    nlp = spacy.load("en_core_web_sm")
    candidate=defaultdict(int)
    filter=set(["of","speech","score","dir","ever","dressed","nominee","i","we","alive","rubs","my","amazing","like","he","she","it","twitter","awkward","parts","show","insults","part"])
    end_indicator=set(["award","goes",".","receive","golden","goldenglobes","category","wins","at","win","winner"])
    counter=0
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        for i in range(len(lis)):
            if lis[i]=="best" and i<len(lis)-1:
                for j in range(i+1,len(lis)):
                    if lis[j] in filter:
                        break
                    if lis[j] in end_indicator and j>i+1:
                        extract=' '.join(lis[i:j])
                        extract=extract.replace("miniseries","mini-series")
                        extract=extract.replace("seriestv","series television")
                        extract = extract.replace("tv", "television")
                        #print(extract)
                        candidate[extract]+=1
                        counter+=1
                        break
    for ele in candidate:
        if candidate[ele]>=20:
            print(ele,candidate[ele])

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
    find_host(c)
    print("success")

if __name__ == '__main__':
    main()

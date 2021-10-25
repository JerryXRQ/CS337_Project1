'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk

def find_award(container):
    nlp = spacy.load("en_core_web_sm")
    candidate=defaultdict(int)
    filter=set(["buy","movie","hotel","friend","moments","of","speech","score","dir","ever","dressed","nominee","i","we","alive","rubs","my","amazing","like","he","she","it","twitter","awkward","parts","show","insults","part"])
    end_indicator=set(["made","by","for","awarded",'-',"is","award","goes",".","receive","golden","goldenglobes","category","wins","at","win","winner"])
    counter=0
    male_names = nltk.corpus.names.words('male.txt')
    female_names = nltk.corpus.names.words('female.txt')
    n=set(male_names+female_names)
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        for i in range(len(lis)):
            if lis[i]=="best" and i<len(lis)-1:
                for j in range(i+1,len(lis)):
                    if lis[j] in filter:
                        break
                    if lis[j]=="":
                        break
                    if lis[j][-1]=="-" and lis[j]!="-":
                        target = lis[i:j+1]
                        extract = ' '.join(target)
                        extract = extract.replace("miniseries", "mini-series")
                        extract = extract.replace("telecision", "television series")
                        extract = extract.replace("seriestv", "television series")
                        extract = extract.replace("tv", "television series")
                        extract = extract.replace("series series", "series")
                        extract = extract.replace("musical or comedy", "comedy or musical")
                        candidate[extract] += 1
                        counter += 1
                        break
                    if lis[j] in end_indicator or lis[j].capitalize() in n:
                        if j<i+3:
                            break
                        target=lis[i:j]
                        extract=' '.join(target)
                        extract=extract.replace("miniseries","mini-series")
                        extract = extract.replace("telecision", "television series")
                        extract=extract.replace("seriestv","television series")
                        extract = extract.replace("tv", "television series")
                        extract = extract.replace("series series", "series")
                        extract = extract.replace("musical or comedy", "comedy or musical")
                        candidate[extract]+=1
                        counter+=1
                        break


    keys=[k for k in candidate.keys()]
    keys.sort(key=lambda x: candidate[x],reverse=True)

    return keys[:min(len(keys),22)]





def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    c=data.container("2013")
    find_host(c)
    print("success")

if __name__ == '__main__':
    main()

'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util
from imdb import IMDb

def narrow_search(container,award):
    reduce = util.process_name(award)
    key_word = set(["nominee","nominees", "nominate", "nominates", "nominated", "nomination"])
    selected=[]
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        s=set(lis)
        det1=True
        det2=False
        for words in reduce:
            if words=="tv":
                if "tv" in s or "television" in s:
                    continue
            elif words not in s:
                det1=False
                break
        if not det1:
            continue
        for kw in key_word:
            if kw in s:
                det2=True
        if det2:
            selected.append(lis)
    return selected

def broad_search(container,award):
    reduce = util.expand_search(award)
    key_word = set(["nominee","nominees", "nominate", "nominates", "nominated", "nomination"])
    filter=set(["present","presenter","presenting","copresent","presents","presented"])
    selected = []
    for ele in container.keys():
        m = container.get(ele)
        lis = m.get_text()
        s = set(lis)
        det1 = True
        det2 = False
        for words in reduce:
            if words == "tv":
                if "tv" in s or "television" in s:
                    continue
            elif words not in s:
                det1 = False
                break
            if words in filter:
                det1=False
                break
        if not det1:
            continue
        for kw in key_word:
            if kw in s:
                det2 = True
        if det2:
            selected.append(lis)
    return selected

def find_person(tweets):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    for tweets in tweets:
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                dic[ent.text] += 1
    return dic
                # print(ent.text)

def find_object(tweets):
    dic=defaultdict(int)
    ia = IMDb()
    for ele in tweets:
        cut=[]
        for i in range(len(ele)):
            if ele[i]=="nominee" or ele[i]=="nominees" or ele[i]=="nominate" or ele[i]=="nominates":
                cut=ele[i+1:]
                break
            elif ele[i]=="nominated" or ele[i]=="nomination":
                cut=ele[:i]
                break
        print(cut)
        for words in cut:
            res=ia.search_movie(words)
            if res and "2013" in res[0]['long imdb title']:
                print(res)



    return dic


def find_nominee(container,award):
    selected=narrow_search(container,award)
    if len(selected)<5:
        selected=broad_search(container,award)

    dic=None
    if "actor" in award or "actress" in award or "director" in award:
        dic = find_person(selected)

    else:
        dic=find_object(selected)

    k=[k for k in dic.keys()]
    k.sort(key=lambda x:dic[x],reverse=True)
    #print(k)


    for j in range(min(5,len(k))):
       print(k[j])
    return





def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama',
                            'best performance by an actress in a motion picture - drama',
                            'best performance by an actor in a motion picture - drama',
                            'best motion picture - comedy or musical',
                            'best performance by an actress in a motion picture - comedy or musical',
                            'best performance by an actor in a motion picture - comedy or musical',
                            'best animated feature film', 'best foreign language film',
                            'best performance by an actress in a supporting role in a motion picture',
                            'best performance by an actor in a supporting role in a motion picture',
                            'best director - motion picture', 'best screenplay - motion picture',
                            'best original score - motion picture', 'best original song - motion picture',
                            'best television series - drama',
                            'best performance by an actress in a television series - drama',
                            'best performance by an actor in a television series - drama',
                            'best television series - comedy or musical',
                            'best performance by an actress in a television series - comedy or musical',
                            'best performance by an actor in a television series - comedy or musical',
                            'best mini-series or motion picture made for television',
                            'best performance by an actress in a mini-series or motion picture made for television',
                            'best performance by an actor in a mini-series or motion picture made for television',
                            'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                            'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

    file="gg2013.json"
    input=pd.read_json(file)
    c=data.container(input)
    #find_presenter(c,"best performance by an actor in a television series - comedy or musical")
    #return
    for ele in OFFICIAL_AWARDS_1315:
        print(ele)
        find_nominee(c, ele)
    print("Done")

if __name__ == '__main__':
    main()

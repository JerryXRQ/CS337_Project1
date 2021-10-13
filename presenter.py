'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util
def narrow_search(container,award):
    reduce = util.process_name(award)
    key_word = set(["present", "presented", "presents", "presenting", "presenter","copresent"])
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
    key_word = set(["present", "presented", "presents", "presenting", "presenter", "copresent"])
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
        if not det1:
            continue
        for kw in key_word:
            if kw in s:
                det2 = True
        if det2:
            selected.append(lis)
    return selected


def find_presenter(container,award):
    nlp = spacy.load("en_core_web_sm")
    candidate=defaultdict(int)
    key_word = set(["present", "presented", "presents", "presenting", "presenter", "copresent"])
    #print(reduce)

    selected=narrow_search(container,award)
    if len(selected)==0:
        selected=broad_search(container,award)

    dic=defaultdict(int)
    for tweets in selected:
        sentence=""
        for i in range(len(tweets)):
            if tweets[i] in key_word:
                if i+1<len(tweets) and tweets[i+1]=="by":
                    sentence=" ".join(tweets[i+2:])
                elif tweets[i]=="presenter":
                    sentence=" ".join(tweets)
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
        find_presenter(c, ele)
    print("Done")

if __name__ == '__main__':
    main()

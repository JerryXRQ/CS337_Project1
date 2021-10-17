'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util

def narrow_search(container,award):
    reduce = util.process_name(award)
    key_word = set(["nominee","nominees", "nominate", "nominates", "nominated", "nomination","up for","should win","robbed","deserve","should have won"])
    filter=set(["present","presenter","presenting","copresent","presents","presented","oscar"])
    selected=[]

    #print(reduce)
    if "supporting" not in reduce:
        filter.add("supporting")
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        s=set(lis)
        det1=True
        det2=False
        for words in reduce:
            if words == "tv" or words == "series":
                if "tv" in s or "television" in s or "series" in s:
                    continue
            elif words=="comedy" or words=="musical":
                if "comedy" in s or "musical" in s:
                    continue
            elif words=="motion" or words=="picture":
                if "motion" in s or "picture" in s:
                    continue
            elif words not in s:
                det1=False
                break
        if not det1:
            continue
        detf=True
        for ele in filter:
            if ele in s:
                detf=False
                break
        if not detf:
            continue
        for kw in key_word:
            if kw in s:
                det2=True
        if det2:
            selected.append(lis)
            selected.append(m.get_hashtags())
    return selected

def broad_search(container,award):
    reduce = util.expand_search(award)
    key_word = set(["nominee","nominees", "nominate", "nominates", "nominated", "nomination","up for","should win","robbed","deserve","should have won"])
    filter=set(["present","presenter","presenting","copresent","presents","presented","oscar"])
    selected = []
    if "supporting" not in reduce:
        filter.add("supporting")
    for ele in container.keys():
        m = container.get(ele)
        lis = m.get_text()
        s = set(lis)
        det1 = True
        det2 = False
        for words in reduce:
            if words == "tv" or words=="series":
                if "tv" in s or "television" in s:
                    continue
                if "drama" in reduce and "drama" in s:
                    continue
            elif words=="comedy" or words=="musical":
                if "comedy" in s or "musical" in s:
                    continue
            elif words=="motion" or words=="picture":
                if "motion" in s or "picture" in s:
                    continue
                if "drama" in reduce and "drama" in s:
                    continue
            elif words not in s:
                det1 = False
                break
        if not det1:
            continue
        detf=True
        for ele in filter:
            if ele in s:
                detf=False
                break
        if not detf:
            continue
        for kw in key_word:
            if kw in s:
                det2 = True
        if det2:
            selected.append(lis)
            selected.append(m.get_hashtags())
    return selected

def find_person(tweets):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    filter = set(["golden globe", "the golden globe", "good", "goldenglobes", "series", "you", "tv", "awards",
                  "comedy", "season", "deserve", "award", "drama", "motion", "picture", "movie", "song", "great", "win"
                     , "who", "what", "the", "guy", "tune", "nbc", "est", "askglobes", "ball", "madmen", "miniseriestv",
                  "someone","u","impresssiveeee"])
    strict = set(["miniseriestv","oscar","congrats"])
    for tweets in tweets:
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text not in filter:
                det=True
                for ele in strict:
                    if ele in ent.text:
                        det=False
                if det:
                    dic[ent.text] += 1
    return dic
                # print(ent.text)

def find_object(tweets):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    male_names = nltk.corpus.names.words('male.txt')
    female_names = nltk.corpus.names.words('female.txt')
    n = set(male_names + female_names)
    filter=set(["golden globe","the golden globe","good","goldenglobes","series","you","tv","awards",
                "comedy","season","deserve","award","drama","motion","picture","movie","song","great","win"
                   ,"who","what","the","guy","tune","nbc","est","askglobes","ball","madmen","miniseriestv","someone","u"])
    strict=set(["win","finales","fingers","nomination","really","award","series","pm","tonight","comedy","goldenglobes","motion","picture","movie"
                   ,"animated",'golden',"nominee","nominees","drama","him","their","they","it","congrats","best","winner","congratulations","i","we",
                "his","her","man","woman","boy","girl","girls","part","she","he","so","hmmm","love","outstanding","is","president","song","original",
                "what","bad","oscar","rage"])
    for tweets in tweets:
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for np in doc.noun_chunks:  # use np instead of np.text
            det=True
            if np.text in filter:
                break
            for ele in np.text.split():
                if ele in strict or ele in n:
                    det=False
                    break
            if det:
                dic[np.text]+=1
    return dic



def find_nominee(container,award):
    selected=narrow_search(container,award)
    if len(selected)<5:
        selected=broad_search(container,award)

    dic=None
    if "actor" in award or "actress" in award or "director" in award or "cecil" in award:
        dic = find_person(selected)

    else:
        #print("TAKEN")
        dic=find_object(selected)

    k=[k for k in dic.keys()]
    k.sort(key=lambda x:dic[x],reverse=True)

    res=[]
    for j in range(min(5,len(k))):
        temp=k[j].replace("nominee ","")
        temp = temp.replace("the golden globe", "")
        temp = temp.replace("the golden globe", "")
        temp = temp.replace(" goldenglobes", "")
        res.append(temp)
    print(res)
    return res





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

    c=data.container("2013")
    #find_presenter(c,"best performance by an actor in a television series - comedy or musical")
    #return
    for ele in OFFICIAL_AWARDS_1315:
        print(ele)
        find_nominee(c, ele)
    #print("Done")

if __name__ == '__main__':
    main()
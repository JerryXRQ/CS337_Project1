'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util
import winner
import multiprocessing

def broad_search(container,award):
    reduce = util.expand_search(award)
    key_word = set(["nominee", "nominees", "nominate", "nominates", "nominated", "nomination", "up for",
                    "should win", "robbed", "should have won", "would've won", "sad", "runner"
                    "wish", "hope", "pain","pains","would like", "win","won","wins","winning","goes to","receive"])
    filter=set(["nominee","nominate","nominates","present","presenter","presenting","copresent","presents","presented","oscar","should","hope","should've"])
    selected = []
    if "supporting" not in reduce and ("actor" in reduce or "actress" in reduce):
        filter.add("supporting")
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
            elif words not in s and words+"." not in s:
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
    #print(selected)
    return selected



def search(container,award):
    reduce = util.process_name_nom(award)
    key_word = set(["nominee", "nominees", "nominate", "nominates", "nominated", "nomination", "up for",
                    "should win", "robbed", "should have won", "would've won", "sad", "runner"
                    "wish", "hope", "pain","pains","would like"])
    filter=set(["present","presenter","presenting","copresent","presents","presented","oscar","president"])
    selected=[]
    alternative={"tv":["tv","television","series","shows"],"series":["tv","television","series","shows"],
                 "comedy":["comedy","musical"],"musical":["comedy","musical"],"drama":["drama"],
                 "motion":["motion","picture","film","movie","pic"],"song":["music","song"],
                 "screenplay":["screenplay","script","write"],"actor":["actor","he","man"],
                 "actress":["actress","woman","she"],"director":["director","directs","produce","directing"],
                 "score":["compose","score","composer","background"],"animated":["animated","animation","cartoon"],
                 "picture": ["motion", "picture", "film", "movie", "pic"],"film": ["motion", "picture", "film", "movie", "pic"]}
    exclude={"comedy":["drama"],"musical":"drama","drama":["comedy","musical"]}
    if "supporting" not in reduce and ("actor" in reduce or "actress" in reduce):
        filter.add("supporting")
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        s=set(lis)
        det1=True
        det2=False
        for words in reduce:
            if words in alternative:
                for ele in alternative[words]:
                    if ele not in s:
                        det1=False
                        break
                if words in exclude:
                    for ele in exclude[words]:
                        if ele not in s:
                            det1=True
            else:
                if words not in s:
                    det1=False
            if det1==False:
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
            #print(" ".join(lis))
    return selected

def winner_based(name,container):
    key_word = set(["nominee", "nominees", "nominate", "nominates", "nominated", "nomination", "up for",
                    "should win", "robbed", "should have won", "would've won", "sad", "runner"
                    "wish", "hope", "pain","pains","would like"])
    filter=set(["present","presenter","presenting","copresent","presents","presented","oscar"])
    selected=[]

    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        s=" ".join(lis)
        det2=False
        if name not in s:
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

def find_person(tweets):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    filter = set(["golden globe", "the golden globe", "good", "goldenglobes", "series", "you", "tv", "awards",
                  "comedy", "season", "deserve", "award", "drama", "motion", "picture", "movie", "song", "great", "win"
                , "who", "what", "the", "guy", "tune", "nbc", "est", "askglobes", "ball", "madmen", "miniseriestv",
                  "someone","u","impresssiveeee","hell","dick",'kinda'])
    strict = set(["miniseriestv","oscar","congrats","goldengiobes","yay","lets"])
    for tweets in tweets:
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text not in filter:
                det=True
                for ele in strict:
                    if ele in ent.text:
                        det=False
                if "golden" in ent.text or "globe" in ent.text:
                    det=False
                if det:
                    res=ent.text.replace("best actress ","")
                    res = res.replace("hope ","")
                    res = res.replace(" best actress", "")
                    res = res.replace("best actor ", "")
                    res = res.replace(" best actor", "")
                    res = res.replace(" wins", "")
                    res = res.replace(" won","")
                    dic[res] += 1
    return dic

def find_male(tweets,male_names):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")

    for tweets in tweets:
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                builder=""
                det=False
                for e in ent.text.split():
                    if e.capitalize() in male_names:
                        builder += e + " "
                        det = True
                if det:
                    res=ent.text
                    res=res.replace(" won","")
                    res=res.replace(" wins","")
                    res=res.replace("winner ","")
                    dic[res]+=1
    return dic
                # print(ent.text)

def find_female(tweets,female_names):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")

    for tweets in tweets:
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                builder=""
                det=False
                for e in ent.text.split():
                    if e.capitalize() in female_names:
                        builder+=e+" "
                        det=True
                    if det:
                        res = ent.text
                        res = res.replace(" won", "")
                        res = res.replace(" wins", "")
                        res = res.replace("winner ", "")
                        dic[res] += 1
    return dic

def find_object(tweets,names):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    filter=set(["golden globe","goldenglobe","the golden globe","good","goldenglobes","series","you","tv","awards",
                "comedy","season","deserve","award","drama","motion","picture","movie","song","great","win"
                   ,"who","what","the","guy","tune","nbc","est","askglobes","ball","madmen","miniseriestv","someone",
                "u","anyone","reports","tonightso","us","a farce","kinda","my opinion","the rest","host","abc","hbo"])
    strict=set(["show","drunk","room",'robbedgoldenglobes',"globe","nominations","win","finales","fingers","nomination","really","award","series","pm","tonight","comedy",
                 "goldenglobes","motion","picture","movie","animated",'golden',"nominee","nominees","drama","him","their","they","it","congrats","best","winner","congratulations","i","we",
                "his","her","man","woman","boy","girl","girls","part","she","he","so","hmmm","love","outstanding","is","president","song","original","hell","tonightso"
                "this","what","bad","oscar","rage","amp","every","hell","winner","night","ok","pronunciation","next","news","anything","ovation","me","our","coffins","ampas"
                ,"luck","yay","film","victory","blow","evening","movies","films","success","myself","tv","no","something","everyone","pic","globes","internet",'produce',
                "them","lets","description","hollywood","writers","act","support","person","parents","category","year","fact","win","years","everything","actor",
                "talk","mm","travesty","days","thanks","real","outrage","lol","asap","goals","enjoy","jajaja","woohoo","seasons","classy","its"])
    for tweet in tweets:
        sentence = " ".join(tweet)
        doc = nlp(sentence)
        for np in doc.noun_chunks:  # use np instead of np.text
            det=True
            if np.text in filter:
                break
            for ele in np.text.split():
                if ele in strict or (ele.capitalize() in names and ele!="lincoln"):
                    det=False
                    break
            if det:
                res=np.text
                res.replace(" - ","")
                res.replace("- ","")
                res.replace(" -","")
                dic[res]+=1
    return dic

def new_find_obj(tweets,ref):
    dic=defaultdict(int)
    filter = set(
        ["golden globe", "goldenglobe", "the golden globe", "good", "goldenglobes", "series", "you", "tv", "awards",
         "comedy", "season", "deserve", "award", "drama", "motion", "picture", "movie", "song", "great", "win"
            , "who", "what", "the", "guy", "tune", "nbc", "est", "askglobes", "ball", "madmen", "miniseriestv",
         "someone", "u", "anyone", "reports", "tonightso","1","no",'l', 'ted', 'television', 'hope', 'poe',"abc","hbo"])
    strict = set(["show", "drunk", "room", 'robbedgoldenglobes', "globe", "nominations", "win", "finales", "fingers",
                  "nomination", "really", "award", "series", "pm", "tonight", "comedy",
                  "goldenglobes", "motion", "picture", "movie", "animated", 'golden', "nominee", "nominees", "drama",
                  "him", "their", "they", "it", "congrats", "best", "winner", "congratulations", "i", "we",
                  "his", "her", "man", "woman", "boy", "girl", "girls", "part", "she", "he", "so", "hmmm", "love",
                  "outstanding", "is", "president", "song", "original", "hell", "tonightso"
                                                                                "this", "what", "bad", "oscar", "rage",
                  "amp", "every", "hell", "winner", "night", "ok", "pronunciation", "next", "news", "anything",
                  "ovation", "me", "our", "coffins", "ampas"
                     , "luck", "yay", "film", "victory", "blow", "evening", "movies", "films", "success", "myself",
                  "tv","classy","its"])
    for tweets in tweets:
        sentence = " ".join(tweets)
        for ele in ref:
            if ele.lower() in sentence and ele.lower() not in filter and ele.lower() not in strict :
                dic[ele.lower()]+=1
    return dic

def find_nominee(container,award):

    male_names = nltk.corpus.names.words('male.txt')
    female_names = nltk.corpus.names.words('female.txt')
    n=set(male_names+female_names)

    selected=broad_search(container,award)
    dic=None
    if len(selected)<5:
        target=winner.find_winner(container, award)

        new=winner_based(target,container)
        if "actor" in award or "actress" in award or "director" in award or "cecil" in award:
            dic = find_person(new)

        else:
            dic = find_object(new,n)
        if target in dic:
            dic.pop(target)
    else:
        if "actor" in award or "actress" in award or "director" in award or "cecil" in award:
            dic=find_person(selected)

        else:
            dic=find_object(selected, n)

    k=[k for k in dic.keys()]
    k.sort(key=lambda x:dic[x],reverse=True)

    res=[]
    for j in range(min(5,len(k))):
        temp=k[j].replace("nominee ","")
        temp = temp.replace("the golden globe", "")
        temp = temp.replace("the golden globe", "")
        temp = temp.replace(" goldenglobes", "")
        temp = temp.replace(" amp "," ")
        temp = temp.replace(" lover", "")
        temp = temp.replace("2013", "")
        res.append(temp)
    print(res)
    return res



def run_all(lis,c,dic):

    # find_nominee(c,'best performance by an actor in a supporting role in a motion picture',None)
    # return
    # util.get_movies_year1("2012")
    for ele in lis:
        print(ele)
        dic[ele]=find_nominee(c, ele)

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

    c = data.container("2013")
    l1=[[],[],[],[]]
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for i in range(len(OFFICIAL_AWARDS_1315)):
        l1[i%4].append(OFFICIAL_AWARDS_1315[i])
    p1=multiprocessing.Process(target=run_all,args=(l1[0],c,return_dict))
    p2=multiprocessing.Process(target=run_all,args=(l1[1],c,return_dict))
    p3 = multiprocessing.Process(target=run_all, args=(l1[2], c,return_dict))
    p4 = multiprocessing.Process(target=run_all, args=(l1[3], c,return_dict))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    print(return_dict)

if __name__ == '__main__':
    main()
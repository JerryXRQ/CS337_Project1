'''Version 0.35'''
import data
import spacy
import pandas as pd
from collections import defaultdict
import nltk
import util
import winner


def narrow_search(container,award):
    reduce = util.process_name(award)
    print(reduce)
    key_word = set(["nominee","nominees", "nominate", "nominates", "nominated", "nomination","up for","should win","robbed","deserve","should have won"])
    filter=set(["present","presenter","presenting","copresent","presents","presented","oscar"])
    selected=[]

    #print(reduce)
    if "supporting" not in reduce:
        filter.add("supporting")
    for ele in container.keys():
        m=container.get(ele)
        lis=m.get_text()
        s=" ".join(lis)
        det1=True
        det2=False
        for words in reduce:
            if words == "tv" or words == "series":
                if "tv" in s or "television" in s or "series" in s or "shows" in s:
                    continue
                elif "motion" not in s and "picture" not in s and "movie" not in s and "film" not in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="comedy" or words=="musical":
                if "comedy" in s or "musical" in s or "comed" in s or "music" in s:
                    continue
                elif "drama" not in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="drama":
                if "comedy" in s or "musical" in s or "comed" in s or "music" in s:
                    continue
                elif "comedy" not in s and "musical" not in s:
                    continue
                else:
                    det1=False
                    break

            elif words=="motion" or words=="picture" or words=="film":
                if "motion" in s or "picture" in s or "movie" in s or "film" in s or "pic" in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="song":
                if "music" in s or "song" in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="screenplay":
                if "screen" in s or "write" in s or "script" in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="actor":
                if "he" in s or "actor" in s or "man" in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="actress":
                if "she" in s or "actress" in s or "woman" in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="director":
                if "direct" in s or "directs" in s or "produce" in s or words in s or "directing" in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="score":
                if "score" in s or "compose" in s:
                    continue
                else:
                    det1=False
                    break
            elif words=="animated":
                if "animate" in s or "cartoon" in s or "animation" in s:
                    continue
                else:
                    det1=False
                    break
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
        det1=True
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
    strict = set(["miniseriestv","oscar","congrats","goldengiobes","yay"])
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


def find_object(tweets):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    male_names = nltk.corpus.names.words('male.txt')
    female_names = nltk.corpus.names.words('female.txt')
    n=set(male_names+female_names)
    filter=set(["golden globe","goldenglobe","the golden globe","good","goldenglobes","series","you","tv","awards",
                "comedy","season","deserve","award","drama","motion","picture","movie","song","great","win"
                   ,"who","what","the","guy","tune","nbc","est","askglobes","ball","madmen","miniseriestv","someone","u","anyone","reports","tonightso"])
    strict=set(["show","drunk","room",'robbedgoldenglobes',"globe","nominations","win","finales","fingers","nomination","really","award","series","pm","tonight","comedy",
                 "goldenglobes","motion","picture","movie","animated",'golden',"nominee","nominees","drama","him","their","they","it","congrats","best","winner","congratulations","i","we",
                "his","her","man","woman","boy","girl","girls","part","she","he","so","hmmm","love","outstanding","is","president","song","original","hell","tonightso"
                "this","what","bad","oscar","rage","amp","every","hell","winner","night","ok","pronunciation","next","news","anything","ovation","me","our","coffins","ampas"
                ,"luck","yay","film","victory","blow","evening","movies","films","success","myself","tv","no","something","everyone","pic","globes","internet",'produce',
                "them","lets","description","hollywood","writers","act","support","person","parents","category","year","fact"])
    for tweets in tweets:
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for np in doc.noun_chunks:  # use np instead of np.text
            det=True
            if np.text in filter:
                break
            for ele in np.text.split():
                if ele in strict or (ele.capitalize() in n and ele!="lincoln"):
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
         "someone", "u", "anyone", "reports", "tonightso","1","no",'l', 'ted', 'television', 'hope', 'poe'])
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
                  "tv"])
    for tweets in tweets:
        sentence = " ".join(tweets)
        for ele in ref:
            if ele.lower() in sentence and ele.lower() not in filter and ele.lower() not in strict :
                dic[ele.lower()]+=1
    return dic


def find_nominee(container,award):
    selected=narrow_search(container,award)
    dic=None
    if len(selected)<5:
        target=winner.find_winner(container, award)
        new=winner_based(target,container)
        if "actor" in award or "actress" in award or "director" in award or "cecil" in award:
            dic = find_person(new)

        else:
            dic = find_object(new)
        dic.pop(target)
    else:
        if "actor" in award or "actress" in award or "director" in award or "cecil" in award:
            dic=find_person(selected)

        else:
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


def find_person_alt(tweets, weights):
    hosts = ["amy poehler", "tina fey", "robert pattinson", "amanda seyfried", "halle berry", "aziz ansari",
             "jason bateman", "arnold schwarzenegger", "sylvester stallone", "bradley cooper", "kate hudson",
             "dennis quaid", "kerry washington", "dustin hoffman", "will ferrell", "kristen wiig",
             "don cheadle", "eva longoria", "jennifer lopez", "jason statham", "nathan fillion", "lea michele",
             "george clooney", "robert downey, jr.", "jennifer garner", "julia roberts", "kristen bell", "john krasinski",
             "megan fox", "jonah hill", "salma hayek", "paul rudd", "jessica alba", "kiefer sutherland", "don cheadle",
             "sacha baron cohen", "jennifer lopez", "jason statham", "eva longoria", "george clooney", "jimmy fallon",
             "jay leno", "salma hayek", "paul rudd", "lucy liu", "debra messing"]
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    filter = set(["golden globe", "the golden globe", "good", "goldenglobes", "series", "you", "tv", "awards",
                  "comedy", "season", "deserve", "award", "drama", "motion", "picture", "movie", "song", "great", "win"
                     , "who", "what", "the", "guy", "tune", "nbc", "est", "askglobes", "ball", "madmen", "miniseriestv",
                  "someone","u","impresssiveeee"])
    strict = set(["miniseriestv","oscar","congrats"])
    for i, tweets in enumerate(tweets):
        sentence = " ".join(tweets)
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and ent.text not in filter:
                det=True
                for ele in strict:
                    if ele in ent.text:
                        det=False
                if det:
                    name = ent.text
                    name.replace("-", "")
                    name.replace("   ", " ")
                    name.replace("  ", " ")
                    l = name.split(" ")
                    if len(l) > 2:
                        if f"{l[0]} {l[1]}" not in hosts:
                            dic[f"{l[0]} {l[1]}"] += weights[i]
                    else:
                        dic[name] += weights[i]
    return dic


def get_mul(words_set, award) -> int:
    SEX_MULT, SUPP_MULT, TYPE_MULT = 300, 1000, 500
    MPD, MPCM, TVSD, TVSCM, MINI = ['motion', 'picture', 'drama'], ['motion', 'picture', 'comedy', 'musical'], \
                           ['television', 'series', 'drama'], ['television', 'series', 'comedy', 'musical'], ['mini-series']
    sex = 1 if 'actor' in award else 0
    type_key = None
    if 'mini-series' in award:
        type_key = MINI
    elif 'motion' in award and 'drama' in award:
        type_key = MPD
    elif 'motion' in award and 'comedy' in award:
        type_key = MPCM
    elif 'series' in award and 'drama' in award:
        type_key = MPD
    elif 'series' in award and 'comedy' in award:
        type_key = MPCM
    support = True if 'support' in award else False
    # print(sex, type_key, support)

    if (sex == 1 and 'actor' not in words_set) or (sex == 0 and 'actress' not in words_set):
        return 0

    mul = 0
    addition = 0

    if (sex == 1 and 'actor' in words_set and 'actress' not in words_set) or \
            (sex == 0 and 'actress' in words_set and 'actor' not in words_set):
        addition += SEX_MULT

    if support and 'supporting' in words_set:
        mul += SUPP_MULT + addition

    test = True
    for key in type_key:
        if key not in words_set:
            test = False
            break
    if test:
        mul += TYPE_MULT + addition

    return mul


def find_nominee_performance(container, award):
    selected = []
    weights = []
    for ele in container.keys():
        m = container.get(ele)
        lis = m.get_text()
        s = set(lis)
        mul = get_mul(s, award)
        if mul != 0:
            selected.append(lis)
            weights.append(mul)

    dic = find_person_alt(selected, weights)
    names = list(dic.keys())
    names.sort(key=lambda x: dic[x], reverse=True)

    print(names[:5] if len(names) >= 5 else names)
    return names[:5] if len(names) >= 5 else names


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

    OFFICIAL_AWARDS_1315_PERFORMANCE = ['best performance by an actress in a motion picture - drama',
                                        'best performance by an actor in a motion picture - drama',
                                        'best performance by an actress in a motion picture - comedy or musical',
                                        'best performance by an actor in a motion picture - comedy or musical',
                                        'best performance by an actress in a supporting role in a motion picture',
                                        'best performance by an actor in a supporting role in a motion picture',
                                        'best performance by an actress in a television series - drama',
                                        'best performance by an actor in a television series - drama',
                                        'best performance by an actress in a mini-series or motion picture made for television',
                                        'best performance by an actor in a mini-series or motion picture made for television',
                                        'best performance by an actress in a television series - comedy or musical',
                                        'best performance by an actor in a television series - comedy or musical',
                                        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                                        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

    c=data.container("2013")
    #find_nominee(c,'best performance by an actor in a supporting role in a motion picture',None)
    #return
    for ele in OFFICIAL_AWARDS_1315_PERFORMANCE:
        print(ele)
        find_nominee_performance(c, ele)
    #print("Done")

if __name__ == '__main__':
    main()
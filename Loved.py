# Most Loved celebrity by social media

import data

import pandas as pd
import numpy as np
import re
import json
from collections import defaultdict
import matplotlib.pyplot as plt

from textblob import TextBlob
import spacy


plt.style.use("fivethirtyeight")


def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9+]', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    return text


def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def get_polarity(text):
    return TextBlob(text).sentiment.polarity


def analyze(rating):
    # rating = float(rating)
    if rating > 0:
        return 'positive'
    elif rating < 0:
        return 'negative'
    else:
        return 'zero'


# the one in nominee with minor modification
def find_person(tweets):
    dic = defaultdict(int)
    nlp = spacy.load("en_core_web_sm")
    filter = set(["golden globe", "the golden globe", "good", "goldenglobes", "series", "you", "tv", "awards",
                  "comedy", "season", "deserve", "award", "drama", "motion", "picture", "movie", "song", "great", "win"
                , "who", "what", "the", "guy", "tune", "nbc", "est", "askglobes", "ball", "madmen", "miniseriestv",
                  "someone","u","impresssiveeee","hell","dick",'kinda'])
    strict = set(["miniseriestv","oscar","congrats","goldengiobes","yay","lets"])
    for sentence in tweets:
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


def main():

    # unified data initialization
    c = data.container("2013")

    # using raw strings
    df = pd.DataFrame([c.get(ele).string for ele in c.keys()], columns=["text"])
    df['text'] = df['text'].apply(clean_text)
    df['sub'] = df['text'].apply(get_subjectivity)
    df['polar'] = df['text'].apply(get_polarity)

    # variable setup for analysis
    people = find_person(df['text'].values)
    names = [name for name in people.keys()]
    names.sort(key=lambda x: people[x], reverse=True)
    num_people = 20

    result_dict_sum, result_dict_avg = {}, {}
    for i in range(num_people):

        name = names[i]
        if 'Gold' in name or 'gold' in name or len(name.split(" ")) <= 1:
            continue
        indexes = []
        for j in range(df.shape[0]):
            if name in df['text'][j]:
                indexes.append(j)

        result_dict_sum[name] = np.sum(df['polar'].values[indexes])
        result_dict_avg[name] = np.average(df['polar'].values[indexes])

    result_name_sum = [x for x in result_dict_sum.keys()]
    result_name_sum.sort(key=lambda x: result_dict_sum[x])
    result_score_sum = [x for x in result_dict_sum.values()]
    result_score_sum.sort()

    plt.figure(figsize=(10, 8))
    for i in range(len(result_name_sum)):
        plt.scatter(i, result_score_sum[i], c=result_score_sum[i])
    plt.xlabel("Names")
    plt.ylabel("Sum Polarity")
    plt.title(f"Top {num_people} people's polarity")
    plt.colorbar()
    plt.xticks(np.arange(len(result_name_sum)), result_name_sum)
    plt.savefig("Top Polarity - Sum.png")
    # plt.show()

    result_name_avg = [x for x in result_dict_avg.keys()]
    result_name_avg.sort(key=lambda x: result_dict_avg[x])
    result_score_avg = [x for x in result_dict_avg.values()]
    result_score_avg.sort()

    plt.figure(figsize=(10, 8))
    for i in range(len(result_name_avg)):
        plt.scatter(i, result_score_avg[i], c=result_score_avg[i])
    plt.xlabel("Names")
    plt.ylabel("Sum Polarity")
    plt.title(f"Top {num_people} people's polarity")
    plt.colorbar()
    plt.xticks(np.arange(len(result_name_avg)), result_name_avg)
    plt.savefig("Top Polarity - Avg.png")
    # plt.show()

    print(f"People most loved by social media: {result_name_sum[:num_people // 4]}")

if __name__ == '__main__':
    main()
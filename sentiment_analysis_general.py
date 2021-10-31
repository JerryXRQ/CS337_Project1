# primary source:
# https://www.youtube.com/watch?v=ujId4ipkBio

import data

import pandas as pd
import numpy as np
import re
import json
import matplotlib.pyplot as plt
import sys
from textblob import TextBlob
from wordcloud import WordCloud

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


def get_words_dict(location):
    with open(location) as file:
        data = json.load(file)

    dic = {}

    class Word:
        def __init__(self, row):
            self.word = row[0]
            self.subtitle_freq = row[1]
            self.web_freq = row[2]
            self.syllables = row[3].split(" ")
            self.pos_pct = row[4]
            self.pos = row[5]
            self.vec_pronunciation = [float(x) for x in row[6].split(" ")]
            self.vec_meaning = [float(x) for x in row[7].split(" ")]
            # store self to dic
            dic[self.word] = self

    all_words = [Word(row) for row in data]

    return dic, all_words


def main():
    possible = set(["2013", "2015", "2018", "2019"])
    year = '2013'
    if len(sys.argv) > 1 and sys.argv[1] in possible:
        year = str(sys.argv[1])
    c = data.container(year)

    # unified data initialization
    dic, _ = get_words_dict("all_words_subtlex_small.json")

    # using raw strings
    df = pd.DataFrame([c.get(ele).string for ele in c.keys()], columns=["text"])
    df['text'] = df['text'].apply(clean_text)
    df['sub'] = df['text'].apply(get_subjectivity)
    df['polar'] = df['text'].apply(get_polarity)
    df['analysis'] = df['polar'].apply(analyze)

    # using preprocessed text list
    # df_alt = pd.DataFrame([" ".join(c.get(ele).text) for ele in c.keys()], columns=["text"])
    # df_alt['sub'] = df_alt['text'].apply(get_subjectivity)
    # df_alt['polar'] = df_alt['text'].apply(get_polarity)
    # df_alt['analysis'] = df_alt['text'].apply(analyze)

    # word could visualization
    combined = ' '.join([txt for txt in df['text']])
    word_cloud = WordCloud(width=800, height=600, random_state=21, max_font_size=150).generate(combined)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('wordcloud')
    # plt.show()

    # sort by analysis
    df_sorted = df.sort_values(by=['polar'], ascending=False)
    df_pos = df_sorted[df_sorted['analysis'] == 'positive']
    df_neg = df_sorted[df_sorted['analysis'] == 'negative']
    df_zero = df_sorted[df_sorted['analysis'] == 'zero']

    # polar vs sub visualization
    plt.figure(figsize=(8, 6))
    for i in range(df.shape[0] // 100):
        plt.scatter(df['polar'][i * 100], df['sub'][i * 100], c=[[abs(df['polar'][i * 100]), df['sub'][i * 100], 0.5]])
    plt.title('Sentiment Analysis')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    plt.savefig('polar vs sub')
    # plt.show()

    # common sentiment (single word) used
    subset = df_pos.head(n=100)
    words = ' '.join([txt for txt in subset['text']]).split(' ')
    result = []
    for word in words:
        if word.upper() in dic.keys() and dic[word.upper()].pos in ["Adjective", "Adverb"]:
            result.append(word.lower())
    print(f"Commonly used single sentiment words (positive) are: {str(set(result))}\n")

    # most positive tweets
    tweets = df_pos['text'].values
    print(f"""Most positive tweets:
            {tweets[0]}
            {tweets[1]}
            {tweets[2]}
            {tweets[3]}
            {tweets[4]}\n""")

    # most negative tweets
    tweets = df_neg['text'].values
    print(f"""Most negative tweets:
                {tweets[0]}
                {tweets[1]}
                {tweets[2]}
                {tweets[3]}
                {tweets[4]}\n""")

    # some of neutral tweets
    tweets = df_zero['text'].values
    print(f"""Some of neutral tweets:
                    {tweets[0]}
                    {tweets[1]}
                    {tweets[2]}
                    {tweets[3]}
                    {tweets[4]}\n""")


if __name__ == '__main__':
    main()

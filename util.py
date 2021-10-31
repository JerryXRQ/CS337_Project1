b'''Version 0.35'''
import pandas as pd
import json
import re
import pandas as pd
#import requests
#from bs4 import BeautifulSoup as bs

# File to download and extract:  https://datasets.imdbws.com/title.basics.tsv.gz
path_set = "data.tsv" # path imdb dataset
#df = pd.read_csv(path_set, sep='\t')
def get_movies_year1(year:str):
    df = pd.read_csv(path_set, sep='\t')
    df["startYear"] = df["startYear"].astype(str)
    year_mov = df[df["startYear"] == year]
    year_mov = year_mov[year_mov["titleType"] == "movie"]
    year_mov = year_mov["primaryTitle"].tolist()
    return year_mov

def process_name(award_name):
    award_name.lower()
    new = ""
    filter = '[A-z|0-9| ]'
    for characters in award_name:
        if re.match(filter, characters):
            new += characters
    award_name=new
    name=award_name.replace(" in "," ")
    name=name.replace(" a "," ")
    name=name.replace(" by "," ")
    name=name.replace(" made for "," ")
    name=name.replace("television","tv")
    name=name.replace(" an "," ")
    name=name.replace(" or "," ")
    name=name.replace(" - "," ")
    name=name.replace("-"," ")
    name=name.replace(" role "," ")
    name=name.replace(" miniseries "," ")
    name = name.replace(" performance ", " ")
    name = name.replace("best ", "")
    return name.split()

def process_name_nom(award_name):
    award_name.lower()
    new = ""
    filter = '[A-z|0-9| ]'
    for characters in award_name:
        if re.match(filter, characters):
            new += characters
    award_name=new
    if "screenplay" in award_name:
        return ["screenplay"]

    if "screenplay" in award_name:
        return ["song"]

    if "animated" in award_name:
        return ["animated"]

    if "score" in award_name:
        return ["score"]

    if "foreign" in award_name:
        return ["foreign","film"]

    if "director" in award_name:
        return ["director"]


    name=award_name.replace(" in "," ")
    name=name.replace(" a "," ")
    name=name.replace(" by "," ")
    name=name.replace(" made for "," ")
    name=name.replace("television","tv")
    name=name.replace(" an "," ")
    name=name.replace(" or "," ")
    name=name.replace(" - "," ")
    name=name.replace("-"," ")
    name=name.replace(" role "," ")
    name=name.replace(" miniseries "," ")
    name = name.replace(" performance ", " ")
    name = name.replace("best ", "")
    name=name.replace("original ","")
    return name.split()

def expand_search(award_name):
    lis=process_name(award_name)
    n=[]
    for ele in lis:
        if ele=="motion" or ele=="picture" or ele=="series":
            continue
        else:
            n.append(ele)
    return n

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
    for ele in OFFICIAL_AWARDS_1315:
        print(process_name_nom(ele))

if __name__ == '__main__':
    main()

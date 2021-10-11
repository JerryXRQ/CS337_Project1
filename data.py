'''Version 0.35'''
import pandas as pd
import json
import re
from datetime import datetime

class message(object):
    def __init__(self,raw):
        self.hashtags=[]
        self.text=[]

        filter='[A-z|0-9|-]'
        s=set(["GoldenGlobes","goldenglobes","globes","golden"])
        for words in raw['text'].split(' '):
            if len(words)==0:
                continue
            if words.lower()=="rt":
                continue
            if words[0]=="#" and words[1:] not in s:
                self.hashtags.append(words[1:].lower())
            elif words[:4]=="http" or words[:3]=="www" or words[0]=="@":
                continue
            else:
                new=""
                for characters in words:
                    if re.match(filter,characters):
                        new+=characters
                if len(new)>0:
                    self.text.append(new.lower())
        #print(self.hashtags,self.text)
    def get_text(self):
        return self.text

    def get_hashtags(self):
        return self.hashtags


class container(object):
    def __init__(self,input):
        self.dic=dict()
        curr=0
        sample=input.sample(min(len(input),200000))
        ten=len(sample)//10
        counter=0
        for i,r in sample.iterrows():
            self.dic[r.id]=message(r)

            if counter%ten==0:
                print(curr,"% Finished Processing")
                curr+=10
            counter += 1
            #print(str(r.timestamp_ms))
    def keys(self):
        return self.dic.keys()


    def get(self,key):
        return self.dic[key]


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    file="gg2015.json"
    input=pd.read_json(file)
    temp=container(input)

if __name__ == '__main__':
    main()

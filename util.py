'''Version 0.35'''
import pandas as pd
import json
import re
from datetime import datetime

def process_name(award_name):
    award_name.lower()
    name=award_name.replace(" in "," ")
    name=name.replace(" a "," ")
    name=name.replace(" by "," ")
    name=name.replace(" made for "," ")
    name=name.replace("televison","tv")
    name=name.replace(" an "," ")
    name=name.replace(" or "," ")
    name=name.replace(" - "," ")
    name=name.replace("-","")
    name = name.replace(" performance ", " ")
    name = name.replace("best ", "")
    return name.split()


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

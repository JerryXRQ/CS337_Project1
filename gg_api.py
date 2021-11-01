'''Version 0.35'''
import award
import data
import host
import nominee
import presenter
import winner
import pandas as pd
import multiprocessing
#import sentiment_analysis
import json
import sys

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts=host.find_host(container)
    print(year + " hosts finished")
    return hosts



def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards=award.find_award(container)
    print(year+" awards finished")
    return awards

def run_all_nominees(lis,dic,c):

    # find_nominee(c,'best performance by an actor in a supporting role in a motion picture',None)
    # return
    # util.get_movies_year1("2012")
    for ele in lis:
        #print(ele)
        dic[ele]=nominee.find_nominee(c, ele)

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees={}
    if year=='2013' or year=='2015':
        l1 = [[], [], [], []]
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        for i in range(len(OFFICIAL_AWARDS_1315)):
            l1[i % 4].append(OFFICIAL_AWARDS_1315[i])
        p1 = multiprocessing.Process(target=run_all_nominees, args=(l1[0], return_dict,container))
        p2 = multiprocessing.Process(target=run_all_nominees, args=(l1[1], return_dict,container))
        p3 = multiprocessing.Process(target=run_all_nominees, args=(l1[2], return_dict,container))
        p4 = multiprocessing.Process(target=run_all_nominees, args=(l1[3], return_dict,container))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        #for ele in OFFICIAL_AWARDS_1315:
            #nominees[ele]=nominee.find_nominee(container,ele)
        nominees=return_dict
    else:
        for ele in OFFICIAL_AWARDS_1819:
            nominees[ele]=nominee.find_nominee(container,ele)

    print(year+" nominees finished")
    return nominees

def run_all_winner(lis,dic,c):

    # find_nominee(c,'best performance by an actor in a supporting role in a motion picture',None)
    # return
    # util.get_movies_year1("2012")
    for ele in lis:
        #print(ele)
        dic[ele]=winner.find_winner(c, ele)

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = {}
    if year == '2013' or year == '2015':
        l1 = [[], [], [], []]
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        for i in range(len(OFFICIAL_AWARDS_1315)):
            l1[i % 4].append(OFFICIAL_AWARDS_1315[i])
        p1 = multiprocessing.Process(target=run_all_winner, args=(l1[0], return_dict, container))
        p2 = multiprocessing.Process(target=run_all_winner, args=(l1[1], return_dict, container))
        p3 = multiprocessing.Process(target=run_all_winner, args=(l1[2], return_dict, container))
        p4 = multiprocessing.Process(target=run_all_winner, args=(l1[3], return_dict, container))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        winners=return_dict
    else:
        for ele in OFFICIAL_AWARDS_1819:
            winners[ele] = winner.find_winner(container, ele)
    print(year+" winners finished")
    return winners

def run_all_presenter(lis,dic,c):

    # find_nominee(c,'best performance by an actor in a supporting role in a motion picture',None)
    # return
    # util.get_movies_year1("2012")
    for ele in lis:
        #print(ele)
        dic[ele]=presenter.find_presenter(c, ele)

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = {}
    if year == '2013' or year == '2015':
        l1 = [[], [], [], []]
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        for i in range(len(OFFICIAL_AWARDS_1315)):
            l1[i % 4].append(OFFICIAL_AWARDS_1315[i])
        p1 = multiprocessing.Process(target=run_all_presenter, args=(l1[0], return_dict, container))
        p2 = multiprocessing.Process(target=run_all_presenter, args=(l1[1], return_dict, container))
        p3 = multiprocessing.Process(target=run_all_presenter, args=(l1[2], return_dict, container))
        p4 = multiprocessing.Process(target=run_all_presenter, args=(l1[3], return_dict, container))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        presenters=return_dict
    else:
        for ele in OFFICIAL_AWARDS_1819:
            presenters[ele] = presenter.find_presenter(container, ele)
    print(year+" presenters finished")
    return presenters

def get_sentiment(names):
    sentiments = dict()
    for i in names:
        sentiments[i] = sentiment_analysis.sentiment(container, i)
    return sentiments

def pre_ceremony(year):
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    global container
    container = data.container(year)
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    possible = set(["2013", "2015", "2018", "2019"])
    year = '2013'
    if len(sys.argv) > 1 and sys.argv[1] in possible:
        year = str(sys.argv[1])
    pre_ceremony(year)


    #pre_ceremony(year)
    host=get_hosts(year)
    award=get_awards(year)
    presenter=get_presenters(year)
    winner=get_winner(year)
    nominee=get_nominees(year)

    awd=OFFICIAL_AWARDS_1315
    if year=="2018" or year=="2019":
        awd=OFFICIAL_AWARDS_1819
    res={}
    res["Host"]=host
    for ele in awd:
        res[ele]={"Award":ele,"Presenter":presenter[ele],"Nominees":nominee[ele],"Winner":winner[ele]}
    with open(year+' output.json', 'w') as outfile:
        json.dump(res, outfile)

    #sentim = get_sentiment(winner.values())

    #print("Hosts: ",host[0],"  ",host[1])
    #for ele in OFFICIAL_AWARDS_1315:
        #print("Award: ",ele)
        #print("Presenter: ",", ".join(presenter[ele]))
        #print("Nominee: ", ", ".join(nominee[ele]))
        #print("Winner: ",winner[ele])
        #print("Sentiment: ", sentim[winner[ele]])
    #return

if __name__ == '__main__':
    main()

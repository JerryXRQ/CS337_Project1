# gg-project-master
Golden Globe Project Master

The packages necessary to run our code are included in the file finalized_requirements.txt. However, the following packages might require separate installation.

For spacy, we need to install en_core_web_sm via python -m spacy download en.
For nltk, we need to add the names files with command python -m nltk.downloader names
For textblob, we need to download necessary data by running python -m textblob.download_corpora

To run the autograder, simply use the command python autograder.py (+year).

To make the runtime more manageable, we enabled multiprocessing in our code. The multithreading is performed in gg_api.py on tasks nominee, winner, and presenter. In case multiprocessing cause problems when running our code, we included the single-threaded version of gg_api.py. By replacing everything in gg_api.py with the content of gg_api_single_thread.py, the code will run in single-threaded mode.

We also included some different approaches we have attempted for the tasks. For nominees.py, we created selected sets of movie names, TV series names, actor names, actress names, and director names, which were used to match the content of the tweets. However, because of the runtime requirements, we could not use it in our final submission. This method should be able to improve the overall performance on that task. You can see our attempt in nominee-modified.py.

The extra tasks we attempted include the following.

Humor Detection

We implemented humor detection. This code finds the people who made the best jokes through keyword search. It also includes a naive attempt at finding the subject of the joke by finding common elements in the selected tweets.

To run the code, use the command python humor.py. You can add a year after the input to control which year the code runs on. If that input is not provided, it will choose 2013 by default.

 Red Carpet - Best Dressed and Worst Dressed

 We implemented best dressed and worse dressed analysis. This code uses keyword search and sentiment analysis to find the best and worse dressed. It also finds the most discussed person on Twitter. Additionally, we integrated Bing downloader to directly find pictures of the selected people online. However, this service is not stable. If the code detects errors, it will print "Something when wrong when retrieving images from Bing". Other functions should always run normally.

To run the code, use the command python red_carpet.py. You can add a year after the input to control which year the code runs on. If that input is not provided, it will choose 2013 by default.

Parties - Best Party Hosts

We implemented a program that tracks the most discussed parties of a given year. However, because the source data only includes a small time segment, many parties were not recorded. Therefore, the quality of data produced was limited.

To run the code, use the command python parties.py. You can add a year after the input to control which year the code runs on. If that input is not provided, it will choose 2013 by default. It requires "vader_lexicon" package of nltk, but the code can download it automatically.

Sentiment Analysis - Sentiment towards a Person

We implemented a program that evaluates the sentiment score of the public for a given person in a given year. It returns a score that reflects the average sentiment. A positive value reflects positive sentiment and a negative value reflects negative sentiment.

To run the code, use the command python parties.py. You need to add a year and a name after the file name to control which target the code runs on. It requires "vader_lexicon" package of nltk, but the code can download it automatically.

Some reference performance:

Because we use sampling, the scores we get tend to be not stable. The following are results from five consecutive runs. It should reflect our average case performance.

Test Environment: Harley Server
Run Time: 4 min
Performance:
'2013': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.7511796676639619, 'completeness': 0.25270270270270273}, 'nominees': {'spelling': 0.34976281689325167, 'completeness': 0.07862142857142856}, 'presenters': {'spelling': 0.46153846153846156, 'completeness': 0.3237179487179487}, 'winner': {'spelling': 0.6153846153846154}}

'2015': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.7476993027915592, 'completeness': 0.3157142857142857}, 'nominees': {'spelling': 0.39444444444444443, 'completeness': 0.09447142857142858}, 'presenters': {'spelling': 0.4391025641025641, 'completeness': 0.3173076923076923}, 'winner': {'spelling': 0.6399161735700198}}

Run Time: 4 min
performance:
'2013': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.7650073118497129, 'completeness': 0.22368421052631576}, 'nominees': {'spelling': 0.38322945255937585, 'completeness': 0.09643095238095238}, 'presenters': {'spelling': 0.4230769230769231, 'completeness': 0.3064102564102564}, 'winner': {'spelling': 0.5769230769230769}}

'2015': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.747699302791559, 'completeness': 0.3157142857142857}, 'nominees': {'spelling': 0.27845827048768224, 'completeness': 0.08443333333333333}, 'presenters': {'spelling': 0.3042929292929293, 'completeness': 0.26346153846153847}, 'winner': {'spelling': 0.6014546351084813}}

Run Time: 4 min
Performance:
'2013': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.7650073118497129, 'completeness': 0.22368421052631576}, 'nominees': {'spelling': 0.34976281689325167, 'completeness': 0.0780142857142857}, 'presenters': {'spelling': 0.4230769230769231, 'completeness': 0.3064102564102564}, 'winner': {'spelling': 0.5769230769230769}}

'2015': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.7550957524957013, 'completeness': 0.32499999999999996}, 'nominees': {'spelling': 0.44185457516339866, 'completeness': 0.09690000000000001}, 'presenters': {'spelling': 0.3758741258741259, 'completeness': 0.26794871794871794}, 'winner': {'spelling': 0.6014546351084813}}

Run Time: 4 min
Performance
'2013': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.7650073118497129, 'completeness': 0.22368421052631576}, 'nominees': {'spelling': 0.3934255309907484, 'completeness': 0.09481190476190475}, 'presenters': {'spelling': 0.46153846153846156, 'completeness': 0.3237179487179487}, 'winner': {'spelling': 0.5769230769230769}}

'2015': {'hosts': {'spelling': 1.0, 'completeness': 1.0}, 'awards': {'spelling': 0.7476993027915593, 'completeness': 0.3157142857142857}, 'nominees': {'spelling': 0.4682961972667855, 'completeness': 0.10639761904761907}, 'presenters': {'spelling': 0.4051659125188537, 'completeness': 0.27147435897435895}, 'winner': {'spelling': 0.6399161735700198}}

import praw 
import csv
import collections
import matplotlib.pyplot as pypl

tickerList =[]
realTickerList = []
tickersFound = []
removeTickerList = ['A','ANY','BIG','CARE','DO','FOR','IT','KIDS','ON','OR','ROLL','SEE','TWO','HAS','ALL','BE','EARN','GO','HE','I','JOB','BY','STAY','NICE','NEXT','FAT','VERY','TECH','FUND','SAVE','POST','PLAY','RUN', 'ARE',
                    'TELL','ONE','AT','ERIC','GOOD','LOW','ONE','BEST','OUT','AN','TRUE','TYPE','THOR','BEAT','WELL','SO','PER','NOW','JOBS','CEO','ACT','REAL','AM','ROAD','NEW','ONCE','RH','ELSE','EVER','CASH','TURN','EARS',
                    'SAFE','HOPE','LIFE','LAZY','HOME','INFO','TOO','ERA','EYE','LIVE','WORK','RING','WASH','DD','FAST','FIVE','LOVE','OLD','HEAR','DOOR','KEY','MAIN','MARK','MIND','RARE','ROSE','TREE','COST','GAIN','GRID',
                    'GROW','PLAN','AGE','FORM','BIT','PUMP','RAMP','HI','MET','MAN','LAWS','WINS','FUN','BIO','GOLD','FLOW','SKY','MOD','SPOT','MEET','SITE','ROCK','EAT','LOAN','VIA', 'BEN', 'USA', 'AUTO', 'FLY','AIR','APPS',
                    'CORE', 'GLAD', 'CARS', 'HOOK', 'CAR', 'AIM', 'GOLF', 'AGO', 'PAYS', 'GDP', 'BLUE', 'SUM', 'FLAT']
goodKeywords = []
badKeywords = []

reddit = praw.Reddit(client_id='YiB7E1qC3zWBnQ', client_secret='pX17xnB_99muql3sq2MSb0sqFcA', user_agent='Webscrape')

def readCSV(): # 1    
    print("Reading CSV File...")
    with open('stonks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                tickerList.append(row[0])
                #print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]}.')
                line_count += 1
        print(f'Done. Processed {line_count} lines.')

def removeBadTickers(): # 2
    print("Removing tickers that are also words...")
    for ticker in tickerList:
        score = 0
        for ticka in removeTickerList:
            if ticker == ticka:
                score += 1
        if score == 0:
            realTickerList.append(ticker)
    print("Done.")

def getPosts(): # 3
    print("Retrieving posts...")
    wsbPosts = reddit.subreddit('wallstreetbets').hot(limit=50)
    smPosts = reddit.subreddit('stockmarket').hot(limit=30)
    stockPosts = reddit.subreddit('stocks').hot(limit=30)
    underPosts = reddit.subreddit('undervalued').hot(limit=10)
    invPosts = reddit.subreddit('investing').hot(limit=50)
    rhPosts = reddit.subreddit('robinhood').hot(limit=20)
    print("Done.")
    print("Setting up all posts...")
    setPosts(wsbPosts)
    setPosts(smPosts)
    setPosts(stockPosts)
    setPosts(underPosts)
    setPosts(invPosts)
    setPosts(rhPosts)
    

def setPosts(listPosts): # 4
    for post in listPosts:
        post.selftext = post.selftext.upper()
        post.title = post.title.upper()
        titleList = post.title.split(' ')
        titleList = list(dict.fromkeys(titleList))
        textList = post.selftext.split(' ')
        textList = list(dict.fromkeys(textList))
        tickerCheck(textList, post.num_comments)



def tickerCheck(list, num_comments): # 5
    for ticker in realTickerList:
        for string in list:
            string.replace('$', '')
            string.replace(',', '')
            string.replace('(', '')
            string.replace(')', '')
            string.replace('"', '')
            string.replace("'", '')
            string.replace('.', '')
            string.replace(':', '')
            if ticker == string:
                tickersFound.append(ticker)

def sumTicker():
    print("Adding up tickers...")
    dictTicker = dict.fromkeys(tickersFound)
    dT = collections.OrderedDict(dictTicker)
    noDupeTicker = list(dictTicker)
    
    for nTicker in noDupeTicker:
        loop = 0
        for ticker in tickersFound:
            if nTicker == ticker:
                loop += 1
        dT[str(nTicker)] = loop
    print("Done.")
    print(dT)
    drawGraph(dT)

    
def drawGraph(dictionary):
    values = sorted(dictionary.values(), reverse = True)
    keys = sorted(dictionary.keys(), key=dictionary.__getitem__, reverse = True)
    pypl.bar(keys, values)
    pypl.xticks(rotation = 90)
    pypl.show()

readCSV()
removeBadTickers()
getPosts()
sumTicker()



import praw 
import csv
import collections
import matplotlib.pyplot as pypl

# Give the post a score and rate whether the post is negative towards the stock or positive. 
tickerList =[]
realTickerList = []
tickersFound = []
postsFound = {}
tickersFoundDict = collections.OrderedDict()
removeTickerList = ['I', 'A', 'DD', 'RH', 'CEO', 'FOR', 'ET', 'TV', 'USA', 'AM', 'AI', 'SA', 'NEXT', 'AT']
goodKeywords = ["up", 'moon', 'long', 'buy', 'calls', 'great', 'good', 'underpriced', 'undervalued', 'amazing', 'super', 'terrific', 'excellent', 'awesome', 'strong', 'healthy', 'climb', 'dividend'
                , 'cheap', 'bought', 'hold', 'growth', 'grow', 'strength', 'valuable', 'value', 'plus', 'surge', 'surges', 'deal', 'bull', 'bullish']
badKeywords = ["drop", "drops", "dropped", "down", "plunge", "plunges", "plunged", "nonsense", 'bad', 'overvalued', 'debt', 'overpriced', 'unstable', 'uncertain', 'terrible', 'awful', 'poor'
               , 'unfavourable', 'shit', 'crap', 'burn', 'atrocious', 'short', 'shorting', 'sell', 'puts', 'crash', 'top', 'peaked', 'peak', 'dump', 'damage', 'harm', 'weakness', 'bubble',
              'fraud', 'inflate', 'bear', 'bearish', 'controversy']

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
        titleList = post.title.split(' ')
        titleList = list(dict.fromkeys(titleList))
        textList = post.selftext.split(' ')
        textList = list(dict.fromkeys(textList))
        tickerCheck(textList, post)



def tickerCheck(list, post): # 5
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
                postsFound[post] = ticker

def sumTicker(): #6
    print("Adding up tickers...")
    dictTicker = dict.fromkeys(tickersFound) # turns tickerFound into a dict to remove duplicates
    dT = collections.OrderedDict(dictTicker) # Orders list
    noDupeTicker = list(dictTicker) # turns back into a list with duplicates removed
    
    for nTicker in noDupeTicker:
        loop = 0
        for ticker in tickersFound:
            if nTicker == ticker:
                loop += 1
        dT[str(nTicker)] = loop
    
    print("Done.")
    calculateLikeness()
    print(dT)
    drawGraph(dT)

def calculateLikeness():
    pass
def drawGraph(dictionary): #7
    values = sorted(dictionary.values(), reverse = True)
    keys = sorted(dictionary.keys(), key=dictionary.__getitem__, reverse = True)
    pypl.bar(keys, values)
    pypl.xticks(rotation = 90)
    pypl.show()

readCSV()
removeBadTickers()
getPosts()
sumTicker()



import praw     #for reddit pulls
import datetime as dt
import pandas as pd
from nltk.corpus import words
from sklearn.feature_extraction.text import TfidfVectorizer
from consts import SUBREDIT_SELECTION
from consts import NUMBEROFPULLS
import consts

#warnings.simplefilter(action='ignore')

#-----reddit api authentication-----
def GenFile():
    consts.redditBool = True
    reddit = praw.Reddit(client_id='pF2QPmwUK5v-eymS2gH98w', \
                        client_secret='_ppiPv8sn-hnJQ_-1V91cdsT5xzO2g', \
                        user_agent='Senior Project Class/0.0.1', \
                        username='rfleury', \
                        password='Ryan9543812.')

    #-----use praw to get the topposts-----
    subreddit = reddit.subreddit(SUBREDIT_SELECTION)
    top_subreddit = subreddit.top(limit = NUMBEROFPULLS)

    #-----pick the ammount of posts that would like to be pulled form the subreddit-----
    #for submission in subreddit.top(limit=1):
    #    print(submission.title, submission.id)

    #-----Transform the .json format in your collection into a dataframe-----
    topicsDict = { "title":[], 
                    "score":[], 
                    "id":[], 
                    "url":[],
                    "comms_num": [], 
                    "created": [], 
                    "body":[]}


    #-----appends the data to the dataframe within the correct labled column-----
    for submission in top_subreddit:
        topicsDict["title"].append(submission.title)
        topicsDict["score"].append(submission.score)
        topicsDict["id"].append(submission.id)
        topicsDict["url"].append(submission.url)
        topicsDict["comms_num"].append(submission.num_comments)
        topicsDict["created"].append(submission.created)
        topicsDict["body"].append(submission.selftext)


    #-----creation of topics_data dataframe to hold data-----
    topics_data = pd.DataFrame(topicsDict)
    topics_data= topics_data.drop(labels="title", axis = 1)
    topics_data= topics_data.drop(labels="score", axis = 1)
    topics_data= topics_data.drop(labels="id", axis = 1)
    topics_data= topics_data.drop(labels="url", axis = 1)
    topics_data= topics_data.drop(labels="comms_num", axis = 1)
    topics_data= topics_data.drop(labels="created", axis = 1)


    #-----test print statements-----
    # for word in topics_data:
    #     print(topics_data[word])

    #print(topics_data)

    # #-----import nltk dictionary words-----
    # nltkDictionary = set(nltk.corpus.words.words())#get nltk words dictionary
    # #-----remove words not in nltk words dictionary-----
    # topics_data["body"] = topics_data["body"].apply(lambda x:' '.join([word for word in x.split(' ') if word not in (nltkDictionary)]))

    #-----Remove punctuarion from dataframe entries-----
    #topics_data["title"] = topics_data["title"].str.replace('[^\w\s]','')

    #-----convert the file to a text file to be imputted into the GUI-----
    topics_data["body"].to_csv("RedditPull.txt")

    #-----remove blank lines from text file-----
    output=""
    with open("RedditPull.txt", encoding="utf8") as f:
        for line in f:
            if not line.isspace():
                output+=line
                
    f= open("RedditPull.txt","w", encoding="utf8")
    f.write(output)

    # #-----remove the first two characters of every line of a text file-----
    # with open("RedditSample.txt", "r+") as fin:
    #     lines2 = fin.readlines()
    #     fin.seek(0)
    #     fin.truncate()
    #     for line in lines2:
    #         fin.write(line[2:])
    #     fin.close()

    # #-----removes the first line of a text file-----
    # with open("RedditSample.txt", "r+") as fin:
    #     lines = fin.readlines()
    #     fin.seek(0)
    #     fin.truncate()
    #     fin.writelines(lines[1:])
    #     fin.close()

    





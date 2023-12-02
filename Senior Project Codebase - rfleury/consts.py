#File for constant varriabes present in the program
import random

#MOST IMPORTANT NUMBER IN THE PROGAM!!!
#The larger the feature number the more accuracy the program will have, however
#the bigger this number is the more input text that is required for the program
#to run sucessfully. Number will need to be lowered for smaller amounts of text.
FEATURE_NUMBER = 150

#list of subreddits that random text can be pulled from
#subredditList = ["buildapc", "politics", "shortstories", "Showerthoughts"]

#initialize a random subreddit for the user
#SUBREDIT_SELECTION = random.choice(subredditList)
#print(SUBREDIT_SELECTION)
SUBREDIT_SELECTION = "buildapc"

#varriable fot the ammount
AMMOUNT_TEXT = 10

#indicates the number of posts that will be pulled from reddit
NUMBEROFPULLS = 20

#define a global varriable to indicate if a reddit pull has happened
def init():
    global redditBool
    redditBool = False
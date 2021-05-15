import datetime
import os

#Reddit API Libraries
import praw

#IDEA: get_latest_fresh_posts(): increase performence with threads?
#REddit gives you 600 requests every 10 minutes: 1 request every second

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"], #replace with Reddit API app ID
    client_secret=os.environ["REDDIT_CLIENT_SECRET"], #API app key
    user_agent=os.environ["REDDIT_USER_AGENT"] #from API app
)

#r/subreddit
hiphopheads = reddit.subreddit('HipHopHeads')


#checks that submission on subreddit was within a day -> probably change to a week 
#submission_date_checker(submission: praw.models.Submission): String
def submission_date_checker(submission):        
    range = datetime.datetime.now().date() - datetime.timedelta(days=1)
    submission_time = datetime.datetime.fromtimestamp(submission.created).date()
    if (submission_time >= range):
        return submission.title
    return None


#gets the songs based on Youtube Posts - NOT FINISHED, difficult due to different formats
def get_songs_utube_posts():
    hot_songs = []
    for hot_submission in hiphopheads.hot(limit=1000):
        if ('youtube' in hot_submission.url or 'youtu.be' in hot_submission.url):        
            #hot_songs.append(submission_date_checker(hot_submission))
            try:
                #will split based on AUTHOR - SONGNAME -> however, this isn't the case for every post
                hot_songs.append(submission_date_checker(hot_submission).split('-')[1])
            except IndexError:
                continue
    return hot_songs


#lambda function to remove characters between two characters
get_string = lambda s: s.split('[')[0] + s.split(']')[-1]


#returns array of titles of fresh posts based on if it's fresh or not
#less posts with Fresh tag, larger limit
#get_latest_fresh_posts(): [String]
def get_latest_fresh_posts():
    fresh_posts = []
    for hot_submission in hiphopheads.hot(limit=5000):
        print(hot_submission.title)
        if (
            hot_submission.link_flair_text is not None and 
            (hot_submission.link_flair_text.lower() == "fresh" or hot_submission.link_flair_text.lower() == "fresh video") or 
            "[fresh]" in hot_submission.title.lower() or 
            "[fresh video]" in hot_submission.title.lower()
            ):
                #title = submission_date_checker(hot_submission)
                title = hot_submission.title
                if title is not None:
                    title = get_string(title).strip()
                    fresh_posts.append(title)                                                     
    return fresh_posts


#returns all the hottest posts in r/hiphopheads
#lots of hot posts -> smaller limit
def get_hottest_posts():
    hot_posts = []
    for hot_submission in hiphopheads.hot(limit=1000):
        if hot_submission.title is not None:
            hot_posts.append(get_string(hot_submission.title).strip())                                
    return hot_posts
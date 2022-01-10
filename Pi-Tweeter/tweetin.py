import subprocess
import tweepy
import os

consumer_key = ''
consumer_secret = ''

# Paste access token and access token secret here
access_token = ''
access_token_secret = ''

#from settings import (consumer_key, consumer_secret,
 #                     access_token, access_token_secret)


def tweet():
    # Authenticate
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Media loader
    os.system('convert -rotate 180 -delay 10 -loop 0 image*.jpg zaza.gif')
    media = api.media_upload("/home/pi/zaza.gif")
    
    # Tweet Post
    tweet = "Miaou.     #ISIN :)"
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])


if __name__ == '__main__':
    tweet()

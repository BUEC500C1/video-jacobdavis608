
import tweepy
KEY_FILEPATH = "../access.txt"
import wget
from google.cloud import vision

def twitter_summary():
    tokens = []
    try:
        with open(KEY_FILEPATH, "r") as fp:
            for token in fp.readlines():
                tokens.append(token.rstrip())
    except:
        print("Cannot find Tweepy API keys")
        print("Exiting...")
        return

    access_token, access_token_secret, api_key, api_key_secret = tokens
    
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)
    public_tweets = api.home_timeline(count=100) #get 100 tweets from timeline
    media_files = set()
    for tweet in public_tweets:
        try:
            media = tweet.entities.get('media', [])
            media_files.add(media[0]['media_url'])
        except:
            continue
    
    # Use Google vision to get summary of twitter feed
    summary = []
    summary.append("Hello! Here is a summary of the images on your twitter feed today!")

    tweet_num = 1
    for url in media_files:
        next_message = "Tweet {0}:".format(tweet_num)
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = url

        response = client.label_detection(image=image)
        
        for label in response.label_annotations:
            next_message += f'{label.description} ({label.score*100.:.2f}%),')
        
        summary.append(next_message)

if __name__ == "__main__":
    twitter_summary()
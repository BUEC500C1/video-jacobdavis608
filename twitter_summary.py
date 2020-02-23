
import tweepy
KEY_FILEPATH = "../access.txt"
import wget
#from google.cloud import vision

def twitter_summary(num):
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
    public_tweets = api.home_timeline(count=num) #get 100 tweets from timeline

    media_files = set()
    for tweet in public_tweets:
        media = tweet.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])

if __name__ == "__main__":
    twitter_summary(20)
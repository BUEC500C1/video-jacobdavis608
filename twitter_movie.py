import tweepy
import wget
import os
KEY_FILEPATH = "../access.txt"

def download_ims(urls, low, high):
    '''Download images from indices low to high of the list of urls'''
    if (len(urls) < 1): 
        print("No images to download")
    else:
        return 

def encode(images_path, fps=30, pix_format='yuv420p', out_format='mp4'):
    '''Encode a video from the numbered images at images_path'''
    command = [
        'ffmpeg', '-framerate', '1/3', '-i', 'img%d.png', 
        '-r', '%d' % fps, '-pix_fmt', '%s' % pix_format, 
        'out.%s' % out_format
    ]
    print(' '.join(command))


def generate_text_images():
    return

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
    encode('')
    #twitter_summary(20)
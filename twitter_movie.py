import tweepy
import wget
import os
import threading
import time
KEY_FILEPATH = "../access.txt"

##########################################################
#
#  
#  The machine being used to test this is an Intel Core i5
#    with 2 cores. At any given time it is therefore useful
#    to have subprocessing for generating text in images
#    and one for the rest (downloads can be multithreaded
#    along with encoding)
#    
##########################################################

def download_ims(urls, low, high):
    '''Download images from indices low to high of the list of urls'''
    if (len(urls) < 1): 
        print("No images to download")
    else:
        os.mkdir('./images')
        os.chdir('./images')
        
        for url in urls:
            wget.download(url, './img')

        os.chdir('..') 

def encode(images_path, fps=30, pix_format='yuv420p', out_format='mp4'):
    '''Encode a video from the numbered images at images_path'''
    command = [
        'ffmpeg', '-framerate', '1/3', '-i', 'img%d.png', 
        '-r', '%d' % fps, '-pix_fmt', '%s' % pix_format, 
        'out.%s' % out_format
    ]
    print(' '.join(command))

def generate_text_images():
    '''Launch as a subprocess to occur in parallel with downloads'''
    return

def twitter_movie(num):
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
    media_files = []
    captions = []
    for tweet in public_tweets:
        captions.append(tweet.text)
        media = tweet.entities.get('media', [])
        if(len(media) > 0):
            media_files.append(media[0]['media_url'])
        else:
            media_files.append('') #placeholder for just text tweets

if __name__ == "__main__":
    start_time = time.time()
    twitter_movie(20)
    print("Twitter movie runtime: %.3f s" % (time.time()-start_time))
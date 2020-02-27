import tweepy
import wget
import os
import shutil
import threading
import multiprocessing
import time
import textwrap
import pickle as pkl
from PIL import Image, ImageDraw, ImageFont
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

def download_and_caption(media, background_size=(1280,720)):
    '''Download images using the input media'''
    if (len(media) < 1): 
        print("No images to download")
    else:
        #download the images
        try:
            for key in media.keys():
                img_file = './images/img_raw%d.jpg' % key
                wget.download(media[key][2], img_file) #download image

                #paste image on a white background under caption
                img = Image.open(img_file, 'r')
                img_w, img_h = img.size
                background = Image.new('RGB', background_size, (29, 161, 242))

                bg_w, bg_h = background.size
                offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
                background.paste(img, offset)

                #caption image
                d = ImageDraw.Draw(background)
                font = ImageFont.truetype('./fonts/HelveticaNeue.ttf', 36) #Choose twitter font
                tweet_template = "{0}: \n\n{1}"
                formatted_text = '\n'.join(textwrap.wrap(media[key][0], width=50)) #wrap tweet text
                d.text((10,10), tweet_template.format(media[key][1], formatted_text), font=font, fill=(255, 255, 255))
                
                background.save('./images/img%d.jpg' % key)
                os.remove('./images/img_raw%d.jpg' % key)
                
        except Exception as e:
            print(e)

def init_images_folder():
    '''Set up images folder for processing'''
    if (os.path.isdir('./images')): #remove if already present
            shutil.rmtree('./images')   #remove all contents
    os.mkdir('./images')

def clean_folders():
    '''Function that deletes images folder and output video'''
    if (os.path.isdir('./images')): #remove if already present
        shutil.rmtree('./images')   #remove all contents
    if (os.path.isfile('./out.mp4')):
        os.remove('./out.mp4')

def encode(images_path, fps=30, pix_format='yuv420p', threads=4, out_format='mp4'):
    '''Encode a video from the numbered images at images_path'''
    if (os.path.isfile('./out.mp4')):
        os.remove('./out.mp4')
    command = [
        'ffmpeg', '-framerate', '1/3', '-i', '{0}/img%d.jpg'.format(images_path), 
        '-threads', '%d' % threads, '-r', '%d' % fps, '-pix_fmt', '%s' % pix_format, 
        'out.%s' % out_format
    ]
    com = ' '.join(command)
    os.system(com)

def generate_text_images(text_tweets, im_size=(1280,720)):
    '''Launch as a subprocess to occur in parallel with downloads'''
    tweet_template = "{0}: \n\n{1}"
    if (not os.path.isdir('./images')):
        os.mkdir('./images')
    for num in text_tweets.keys():
        img = Image.new('RGB', im_size, color=(29, 161, 242))      #make a background with twitter color
        font = ImageFont.truetype('./fonts/HelveticaNeue.ttf', 36) #Choose twitter font
        
        d = ImageDraw.Draw(img)
        formatted_text = '\n'.join(textwrap.wrap(text_tweets[num][0], width=50)) #wrap tweet text
        d.text((10,10), tweet_template.format(text_tweets[num][1], formatted_text), font=font, fill=(255, 255, 255))
        img.save('./images/img%d.jpg' % num)

def save_tweets_pickle(api, num_tweets):
    '''Save the home timeline tweets as a pickle file'''
    tweets = api.home_timeline(count=num_tweets)
    with open('sample_tweets.p', 'wb') as pkl_file:
        pkl.dump(tweets, pkl_file)

def load_tweets_pickle():
    '''Load tweets from saved file'''
    with open('sample_tweets.p', 'rb') as pkl_file:
        return pkl.load(pkl_file)

def twitter_movie(num=20, get_new_tweets=True):
    '''Create twitter feed summary for num tweets. Option to get more tweets from twitter'''
    tokens = []
    try: # Try to find keys
        with open(KEY_FILEPATH, "r") as fp:
            for token in fp.readlines():
                tokens.append(token.rstrip())
    except:
        print("Cannot find Tweepy API keys")
        print("Using pre-fetched Tweets")
        get_new_tweets = False

    if (get_new_tweets):
        access_token, access_token_secret, api_key, api_key_secret = tokens
        
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        #Use Tweepy API to get the latest "num" tweets
        api = tweepy.API(auth)

        public_tweets = api.home_timeline(count=num) #get num tweets from timeline    
    else:
        public_tweets = load_tweets_pickle()
    
    media_tweets = {} #dictionary that maps a tweet number to its media url, user name, and text
    text_tweets = {}  #dictionary that maps a tweet number to its text and user name
    for i in range(len(public_tweets)):
        text = public_tweets[i].text
        user = public_tweets[i].user.name
        media = public_tweets[i].entities.get('media', [])
        if(len(media) > 0):
            media_tweets[i] = (text, user, media[0]['media_url'])
        else:
            text_tweets[i] = (text, user)

    #Initialize images folder
    init_images_folder()
    download_thread = threading.Thread(target=download_and_caption, args=(media_tweets,))
    frame_gen_thread = threading.Thread(target=generate_text_images, args=(text_tweets,))

    # Download images and caption them
    download_thread.start()
    frame_gen_thread.start()

    #Generate text images
    download_thread.join()
    frame_gen_thread.join()

    #Generate video
    encode('./images')

if __name__ == "__main__":
    start_time = time.time()
    twitter_movie()
    print("\n\nTwitter movie runtime: %.3f s" % (time.time()-start_time))
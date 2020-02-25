import twitter_movie
import os

def test_download_images():
    '''Use sample tweets to test image downloads'''
    tweets = twitter_movie.load_tweets_pickle()

    twitter_movie.init_images_folder()

    #Get the tweets with media
    media_tweets = {} #dictionary that maps a tweet number to its media url, user name, and text
    media_indices = []
    for i in range(len(tweets)):
        text = tweets[i].text
        user = tweets[i].user.name
        media = tweets[i].entities.get('media', [])
        if(len(media) > 0):
            media_tweets[i] = (text, user, media[0]['media_url'])
            media_indices.append(i)

    twitter_movie.download_and_caption(media_tweets)

    present_imgs = 0
    for ind in media_indices:
        if (os.path.isfile('./images/img%d.jpg' % ind)):
            present_imgs += 1
    
    assert present_imgs == len(media_indices)

    twitter_movie.clean_folders()
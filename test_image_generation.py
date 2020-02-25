import twitter_movie
import os

def test_image_generation():
    '''Use sample tweets to test image generation'''
    tweets = twitter_movie.load_tweets_pickle()
    
    twitter_movie.init_images_folder()

    #Get the tweets without media
    text_tweets = {} #dictionary that maps a tweet number to its user name, and text
    text_indices = []
    for i in range(len(tweets)):
        text = tweets[i].text
        user = tweets[i].user.name
        media = tweets[i].entities.get('media', [])
        if(not (len(media) > 0)):
            text_tweets[i] = (text, user)
            text_indices.append(i)

    twitter_movie.generate_text_images(text_tweets)

    present_imgs = 0
    for ind in text_indices:
        if (os.path.isfile('./images/img%d.jpg' % ind)):
            present_imgs += 1
    
    assert present_imgs == len(text_indices)

    twitter_movie.clean_folders()
import twitter_movie
import os

def test_movie():
    twitter_movie.twitter_movie()
    if (os.path.isfile('./out.mp4')):
        assert 1 == 1
    else:
        assert 0 == 1

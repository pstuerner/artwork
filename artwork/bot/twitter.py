import os
import tweepy


def ClientV1():
    auth = tweepy.OAuth1UserHandler(
        os.environ["TWITTER_API_KEY"],
        os.environ["TWITTER_API_KEY_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )

    return tweepy.API(auth)

def ClientV2():
    return tweepy.Client(
        os.environ["TWITTER_BEARER_TOKEN"],
        os.environ["TWITTER_API_KEY"],
        os.environ["TWITTER_API_KEY_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )

clientV1 = ClientV1()
clientV2 = ClientV2()

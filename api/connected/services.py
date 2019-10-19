from typing import List

import twitter


class TwitterService:

    def __init__(self, config):
        self.api = twitter.Api(
            consumer_key=config['TWITTER_CONSUMER_KEY'],
            consumer_secret=config['TWITTER_CONSUMER_SECRET'],
            access_token_key=config['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=config['TWITTER_ACCESS_TOKEN_SECRET']
        )

    def get_followers(self, user: str) -> List[str]:
        followers = self.api.GetFollowers(screen_name=user)
        return [follower.name for follower in followers]

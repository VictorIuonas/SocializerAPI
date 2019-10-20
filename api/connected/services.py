from typing import List

import twitter
from github3 import login
from github3.orgs import ShortOrganization

from connected.entities import Organization


class TwitterService:

    def __init__(self, config):
        self.api = twitter.Api(
            consumer_key=config['TWITTER_CONSUMER_KEY'],
            consumer_secret=config['TWITTER_CONSUMER_SECRET'],
            access_token_key=config['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=config['TWITTER_ACCESS_TOKEN_SECRET']
        )

    def get_followers(self, user: str) -> List[str]:
        followers = self.api.GetFollowers(screen_name=f'@{user}')
        return [follower.name for follower in followers]


class GitHubService:

    def __init__(self, config):
        self.gh = login(token=config['GITHUB_TOKEN'])

    def get_organizations_for_user(self, user: str) -> List[Organization]:
        orgs = self.gh.organizations_with(user)
        return [self.to_domain(org) for org in orgs]

    @staticmethod
    def to_domain(org: ShortOrganization) -> Organization:
        return Organization(external_id=org.id, name=org.login, id=0)

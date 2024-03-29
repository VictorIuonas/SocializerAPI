from typing import List
from github3 import login
from github3.exceptions import GitHubException
from github3.orgs import ShortOrganization
from twitter import TwitterError, Api

from api.connected.entities import OrganizationEntity
from api.connected.exceptions import ExternalServiceException


class TwitterService:

    def __init__(self, config):
        self.api = Api(
            consumer_key=config['TWITTER_CONSUMER_KEY'],
            consumer_secret=config['TWITTER_CONSUMER_SECRET'],
            access_token_key=config['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=config['TWITTER_ACCESS_TOKEN_SECRET']
        )

    def get_followers(self, user: str) -> List[str]:
        try:
            followers = self.api.GetFollowers(screen_name=f'@{user}')
            return [follower.screen_name for follower in followers]
        except TwitterError as error:
            print(f'from twitter, when getting followers for {user}: {str(error)}')
            raise ExternalServiceException(f'twitter: {error.message}')


class GitHubService:

    def __init__(self, config):
        self.gh = login(token=config['GITHUB_TOKEN'])

    def get_organizations_for_user(self, user: str) -> List[OrganizationEntity]:
        try:
            orgs = self.gh.organizations_with(user)
            return [self.to_domain(org) for org in orgs]
        except GitHubException as error:
            print(f'from github, when getting orgs for {user}: {str(error)}')
            raise ExternalServiceException(f'github: {str(error)}')

    @staticmethod
    def to_domain(org: ShortOrganization) -> OrganizationEntity:
        return OrganizationEntity(name=org.login, id=0, external_id=org.id)

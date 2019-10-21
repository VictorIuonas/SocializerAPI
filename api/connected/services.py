from typing import List
from github3 import login
from github3.exceptions import GitHubException
from github3.orgs import ShortOrganization
from twitter import TwitterError, Api

from connected.entities import OrganizationEntity
from connected.exceptions import ExternalServiceException


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
            return [follower.name for follower in followers]
        except TwitterError as error:
            raise ExternalServiceException(error.message)


class GitHubService:

    def __init__(self, config):
        self.gh = login(token=config['GITHUB_TOKEN'])

    def get_organizations_for_user(self, user: str) -> List[OrganizationEntity]:
        try:
            orgs = self.gh.organizations_with(user)
            return [self.to_domain(org) for org in orgs]
        except GitHubException as error:
            raise ExternalServiceException(str(error))

    @staticmethod
    def to_domain(org: ShortOrganization) -> OrganizationEntity:
        return OrganizationEntity(name=org.login, id=0, external_id=org.id)

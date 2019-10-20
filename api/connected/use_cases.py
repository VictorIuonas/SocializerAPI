from datetime import datetime

from api.connected.entities import DevsConnection


class CreateConnectionDataUseCase:

    def __init__(self, twitter_service, github_service):
        self.twitter_service = twitter_service
        self.github_service = github_service

    def execute(self, dev1: str, dev2: str):
        dev1_followers = self.twitter_service.get_followers(dev1)
        dev2_followers = self.twitter_service.get_followers(dev2)

        print(f'found followers for {dev1}: {dev1_followers}')
        print(f'found followers for {dev2}: {dev2_followers}')

        dev1_orgs = set(self.github_service.get_organizations_for_user(dev1))
        dev2_orgs = set(self.github_service.get_organizations_for_user(dev2))
        common_orgs = list(dev1_orgs & dev2_orgs)

        are_connected = (dev1 in dev2_followers and dev2 in dev1_followers) or (len(common_orgs) > 0)

        return DevsConnection(connected=are_connected, timestamp=datetime.now, organizations=common_orgs)

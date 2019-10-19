from datetime import datetime

from api.connected.entities import DevsConnection


class CreateConnectionDataUseCase:

    def __init__(self, twitter_service):
        self.twitter_service = twitter_service

    def execute(self, dev1: str, dev2: str):
        dev1_followers = self.twitter_service.get_followers(dev1)
        dev2_followers = self.twitter_service.get_followers(dev2)

        are_connected = dev1 in dev2_followers and dev2 in dev1_followers

        return DevsConnection(connected=are_connected, timestamp=datetime.now, organizations=[])

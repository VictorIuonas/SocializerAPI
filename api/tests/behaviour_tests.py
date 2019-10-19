import json
from unittest.mock import patch, MagicMock

from api import api


class TestGetConnection:

    @patch('connected.services.twitter')
    def test_get_two_unconnected_users(self, twitter):
        scenario = self.Scenario(twitter)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()

        scenario.given_a_request_to_see_if_the_two_developers_are_connected()

        scenario.when_sending_the_request()

        scenario.then_the_response_status_code_is(200)
        scenario.then_the_response_will_say_if_the_users_are_connected(False)

    @patch('connected.services.twitter')
    def test_get_connection_for_two_connected_users(self, twitter):
        scenario = self.Scenario(twitter)

        scenario.given_two_existing_developers()
        scenario.given_they_follow_each_other_on_twitter()

        scenario.given_a_request_to_see_if_the_two_developers_are_connected()

        scenario.when_sending_the_request()

        scenario.then_the_response_status_code_is(200)
        scenario.then_the_response_will_say_if_the_users_are_connected(True)

    class Scenario:
        TEST_DEV_NAME1 = 'test name 1'
        TEST_DEV_NAME2 = 'test name 2'

        def __init__(self, twitter=MagicMock()):
            self.twitter = twitter

            self.dev1 = None
            self.dev2 = None

            self.request = None

            self.client = api.test_client()

            self.result = None
            self.response = None

        def given_two_existing_developers(self):
            self.dev1 = self.TEST_DEV_NAME1
            self.dev2 = self.TEST_DEV_NAME2

        def given_they_follow_each_other_on_twitter(self):
            followers_list = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
            followers_list[0].name = self.dev1
            followers_list[1].name = 'another user 1'
            followers_list[2].name = self.dev2
            followers_list[3].name = 'another user 2'
            self.twitter.Api.return_value.GetFollowers.return_value = followers_list

        def given_they_don_t_follow_each_other_on_twitter(self):
            self.twitter.Api.return_value.GetFollowers.return_value = []

        def given_a_request_to_see_if_the_two_developers_are_connected(self):
            self.request = f'/connected/realtime/{self.dev1}/{self.dev2}'

        def when_sending_the_request(self):
            self.response = self.client.get(self.request)

        def then_the_response_status_code_is(self, status_code: int):
            assert self.response.status_code == status_code

        def then_the_response_will_say_if_the_users_are_connected(self, are_connected: bool):
            result_data = json.loads(self.response.data)
            assert result_data['connected'] == are_connected

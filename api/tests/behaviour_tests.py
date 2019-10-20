import json
from unittest.mock import patch, MagicMock

from api import api


class TestGetConnection:

    @patch('connected.services.login')
    @patch('connected.services.twitter')
    def test_get_two_unconnected_users(self, twitter, git_hub_login):
        scenario = self.Scenario(twitter, git_hub_login)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()
        scenario.given_they_don_t_share_any_organizations_on_github()

        scenario.given_a_request_to_see_if_the_two_developers_are_connected()

        scenario.when_sending_the_request()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_say_if_the_users_are_connected(False)

    @patch('connected.services.login')
    @patch('connected.services.twitter')
    def test_get_connection_for_two_twitter_only_connected_users(self, twitter, git_hub_login):
        scenario = self.Scenario(twitter, git_hub_login)

        scenario.given_two_existing_developers()
        scenario.given_they_follow_each_other_on_twitter()
        scenario.given_they_don_t_share_any_organizations_on_github()

        scenario.given_a_request_to_see_if_the_two_developers_are_connected()

        scenario.when_sending_the_request()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_say_if_the_users_are_connected(True)
        scenario.then_the_response_will_contain_an_empty_organizations_list()

    @patch('connected.services.login')
    @patch('connected.services.twitter')
    def test_get_two_unconnected_twitter_users_sharing_orgs_on_github(self, twitter, git_hub_login):
        scenario = self.Scenario(twitter, git_hub_login)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()
        scenario.given_they_share_two_organizations_on_github()

        scenario.given_a_request_to_see_if_the_two_developers_are_connected()

        scenario.when_sending_the_request()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_say_if_the_users_are_connected(True)
        scenario.then_the_response_will_contain_the_shared_organization_names()

    class Scenario:
        TEST_DEV_NAME1 = 'test name 1'
        TEST_DEV_NAME2 = 'test name 2'

        TEST_SHARED_ORG_EXT_ID1 = 13
        TEST_SHARED_ORG_EXT_ID2 = 17
        TEST_SHARED_ORG_NAME1 = 'shared github org1'
        TEST_SHARED_ORG_NAME2 = 'shared github org2'

        TEST_UNIQUE_ORG_ID1 = 19
        TEST_UNIQUE_ORG_ID2 = 23
        TEST_UNIQUE_ORG_NAME1 = 'github org1 unique to one user'
        TEST_UNIQUE_ORG_NAME2 = 'github org2 unique to the other user'

        def __init__(self, twitter=MagicMock(), git_hub_login=MagicMock()):
            self.twitter = twitter
            self.git_hub_login = git_hub_login
            self.git_hub = MagicMock()
            self.git_hub_login.return_value = self.git_hub

            self.dev1 = None
            self.dev2 = None

            self.request = None

            self.client = api.test_client()

            self.result = None
            self.response = None
            self.result_data = None

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

        def given_they_don_t_share_any_organizations_on_github(self):
            self.git_hub.organizations_with.return_value = []

        def given_they_share_two_organizations_on_github(self):
            shared_orgs = [MagicMock(), MagicMock()]
            shared_orgs[0].id = self.TEST_SHARED_ORG_EXT_ID1
            shared_orgs[1].id = self.TEST_SHARED_ORG_EXT_ID2
            shared_orgs[0].login = self.TEST_SHARED_ORG_NAME1
            shared_orgs[1].login = self.TEST_SHARED_ORG_NAME2

            first_orgs = [MagicMock()]
            first_orgs[0].id = self.TEST_UNIQUE_ORG_ID1
            first_orgs[0].login = self.TEST_UNIQUE_ORG_NAME1
            first_orgs.extend(shared_orgs)

            second_orgs = [MagicMock()]
            second_orgs[0].id = self.TEST_UNIQUE_ORG_ID2
            second_orgs[0].login = self.TEST_UNIQUE_ORG_NAME2
            second_orgs.extend(shared_orgs)

            self.git_hub.organizations_with.side_effect = [first_orgs, second_orgs]

        def when_sending_the_request(self):
            self.response = self.client.get(self.request)

        def when_parsing_the_response_data(self):
            self.result_data = json.loads(self.response.data)

        def then_the_response_status_code_is(self, status_code: int):
            assert self.response.status_code == status_code

        def then_the_response_will_say_if_the_users_are_connected(self, are_connected: bool):
            assert self.result_data['connected'] == are_connected

        def then_the_response_will_contain_an_empty_organizations_list(self):
            assert self.result_data['organizations'] == []

        def then_the_response_will_contain_the_shared_organization_names(self):
            response_organizations = self.result_data['organizations']
            assert len(response_organizations) == 2
            assert self.TEST_SHARED_ORG_NAME1 in response_organizations
            assert self.TEST_SHARED_ORG_NAME2 in response_organizations

import json
from unittest.mock import patch, MagicMock

import pytest
from github3.exceptions import GitHubException
from twitter import TwitterError

from api import api


@pytest.mark.unit
class TestGetConnection:

    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_two_unconnected_users(self, twitter_api, git_hub_login):
        scenario = self.Scenario(twitter_api, git_hub_login)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()
        scenario.given_they_don_t_share_any_organizations_on_github()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_say_if_the_users_are_connected(False)

    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_connection_for_two_twitter_only_connected_users(self, twitter_api, git_hub_login):
        scenario = self.Scenario(twitter_api, git_hub_login)

        scenario.given_two_existing_developers()
        scenario.given_they_follow_each_other_on_twitter()
        scenario.given_they_don_t_share_any_organizations_on_github()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_say_if_the_users_are_connected(True)
        scenario.then_the_response_will_contain_an_empty_organizations_list()

    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_two_unconnected_twitter_users_sharing_orgs_on_github(self, twitter_api, git_hub_login):
        scenario = self.Scenario(twitter_api, git_hub_login)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()
        scenario.given_they_share_two_organizations_on_github()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_say_if_the_users_are_connected(True)
        scenario.then_the_response_will_contain_the_shared_organization_names()

    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_connection_with_twitter_and_github_not_working(self, twitter_api, git_hub_login):
        scenario = self.Scenario(twitter_api, git_hub_login)

        scenario.given_two_existing_developers()
        scenario.given_twitter_is_down()
        scenario.given_github_is_down()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_contain_one_error_for_each_service_and_user()

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

        TEST_TWITTER_ERROR = 'twitter error'
        TEST_GITHUB_ERROR = 'error from github'

        def __init__(self, twitter_api_class=MagicMock(), git_hub_login=MagicMock()):
            self.twitter_api = MagicMock()
            self.twitter_api_class = twitter_api_class
            self.twitter_api_class.return_value = self.twitter_api

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
            self.twitter_api.GetFollowers.return_value = followers_list

        def given_they_don_t_follow_each_other_on_twitter(self):
            self.twitter_api.GetFollowers.return_value = []

        def given_twitter_is_down(self):
            self.twitter_api.GetFollowers.side_effect = TwitterError(self.TEST_TWITTER_ERROR)

        def given_github_is_down(self):
            self.git_hub.organizations_with.side_effect = GitHubException(self.TEST_GITHUB_ERROR)

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

        def when_checking_if_the_developers_are_connected(self):
            self.response = self.client.get(f'/connected/realtime/{self.dev1}/{self.dev2}')

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

        def then_the_response_will_contain_one_error_for_each_service_and_user(self):
            response_errors = self.result_data['errors']
            assert response_errors == [
                self.TEST_TWITTER_ERROR, self.TEST_TWITTER_ERROR, self.TEST_GITHUB_ERROR, self.TEST_GITHUB_ERROR
            ]


@pytest.mark.unit
class TestGetRegisteredConnection:

    @patch('connected.repositories.Connection')
    @pytest.mark.skip
    def test_getting_the_connection_history_for_users_with_no_history(self, connection_db_model):
        with self.Scenario(connection_db_model) as scenario:
            scenario.when_getting_the_history_of_the_connection_between_the_developers()

            scenario.then_the_response_status_code_is(200)

            scenario.when_parsing_the_response_data()

            scenario.then_the_response_will_contain_an_empty_list()

    @patch('connected.repositories.Connection')
    @pytest.mark.skip
    def test_getting_the_history_for_two_developers_found_to_not_be_connected(self, connection_db_model):
        with self.Scenario(connection_db_model) as scenario:
            scenario.given_the_users_were_not_connected()

            scenario.when_getting_the_history_of_the_connection_between_the_developers()

            scenario.then_the_response_status_code_is(200)

            scenario.when_parsing_the_response_data()

            scenario.then_the_response_will_contain_the_date_and_not_connected()

    class Scenario:
        TEST_DEV_NAME1 = 'test name 1'
        TEST_DEV_NAME2 = 'test name 2'

        TEST_SHARED_ORG_EXT_ID1 = 13
        TEST_SHARED_ORG_EXT_ID2 = 17
        TEST_SHARED_ORG_NAME1 = 'shared github org1'
        TEST_SHARED_ORG_NAME2 = 'shared github org2'

        def __init__(self, connection_db_model=MagicMock()):
            self.connection = MagicMock()
            self.connection_db_model = connection_db_model

            self.dev1 = None
            self.dev2 = None

            self.request = None

            self.client = api.test_client()

            self.result = None
            self.response = None
            self.result_data = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def given_the_users_were_not_connected(self):
            self.connection_db_model.query.filter.return_value = self.connection
            self.connection.dev1 = self.TEST_DEV_NAME1
            self.connection.dev2 = self.TEST_DEV_NAME2
            self.connection.is_twitter_link = False
            self.connection.organizations = []
            self.connection.timestamp = '12:00'

        def when_getting_the_history_of_the_connection_between_the_developers(self):
            self.response = self.client.get(f'/connected/registered/{self.dev1}/{self.dev2}')

        def when_parsing_the_response_data(self):
            self.result_data = json.loads(self.response.data)

        def then_the_response_status_code_is(self, status_code: int):
            assert self.response.status_code == status_code

        def then_the_response_will_contain_an_empty_list(self):
            assert self.result_data == []

        def then_the_response_will_contain_the_date_and_not_connected(self):
            assert self.result_data[0]['connected'] == False
            assert self.result_data[0].get('registered_at', None) is not None

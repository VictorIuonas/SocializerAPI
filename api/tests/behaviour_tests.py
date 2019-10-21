from unittest.mock import patch, MagicMock, call

import pytest
from github3.exceptions import GitHubException
from twitter import TwitterError

from api import api
from tests.utils import HttpScenario, ExternalServicesScenario


@pytest.mark.unit
class TestGetConnection:

    @patch('connected.repositories.Connection')
    @patch('connected.repositories.db')
    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_two_unconnected_users(self, twitter_api, git_hub_login, db, connection_db_class):
        scenario = self.Scenario(twitter_api, git_hub_login, db, connection_db_class)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()
        scenario.given_they_don_t_share_any_organizations_on_github()
        scenario.given_the_db_object_stores_the_developers_as_unconnected()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_response_will_say_if_the_users_are_connected(False)
        scenario.then_the_result_will_be_saved_to_the_db_as_unconnected()

    @patch('connected.repositories.Connection')
    @patch('connected.repositories.db')
    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_connection_for_two_twitter_only_connected_users(
            self, twitter_api, git_hub_login, db, connection_db_class
    ):
        scenario = self.Scenario(twitter_api, git_hub_login, db, connection_db_class)

        scenario.given_two_existing_developers()
        scenario.given_they_follow_each_other_on_twitter()
        scenario.given_they_don_t_share_any_organizations_on_github()
        scenario.given_the_db_object_stores_the_developers_as_connected_with_no_common_organizations()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_result_will_be_saved_to_the_db_as_connected()

        scenario.then_the_response_will_say_if_the_users_are_connected(True)
        scenario.then_the_response_will_contain_an_empty_organizations_list()

    @patch('connected.repositories.Organization')
    @patch('connected.repositories.Connection')
    @patch('connected.repositories.db')
    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_two_unconnected_twitter_users_sharing_orgs_on_github(
            self, twitter_api, git_hub_login, db, connection_db_class, organization_db_class
    ):
        scenario = self.Scenario(twitter_api, git_hub_login, db, connection_db_class, organization_db_class)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()
        scenario.given_they_share_two_organizations_on_github()
        scenario.given_the_db_object_stores_the_developers_as_connected_with_their_shared_organizations()
        scenario.given_the_db_object_already_stored_only_one_of_the_shared_organizations()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_db_will_be_queried_for_each_shared_organization()
        scenario.then_the_result_will_be_saved_to_the_db_as_connected()
        scenario.then_the_other_shared_organization_will_be_added_to_the_db()
        scenario.then_the_connection_object_will_contain_the_two_shared_organizations_db_object()

        scenario.then_the_response_will_say_if_the_users_are_connected(True)
        scenario.then_the_response_will_contain_the_shared_organization_names()

    @patch('connected.repositories.Organization')
    @patch('connected.repositories.Connection')
    @patch('connected.repositories.db')
    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_connection_for_two_connected_users_twice_will_store_in_the_database_only_one_connection(
            self, twitter_api, git_hub_login, db, connection_db_class, organization_db_class
    ):
        scenario = self.Scenario(twitter_api, git_hub_login, db, connection_db_class, organization_db_class)

        scenario.given_two_existing_developers()
        scenario.given_they_don_t_follow_each_other_on_twitter()
        scenario.given_they_share_two_organizations_on_github()
        scenario.given_the_db_object_stores_the_developers_as_connected_with_their_shared_organizations()

    @patch('connected.repositories.db')
    @patch('connected.services.login')
    @patch('connected.services.Api')
    def test_get_connection_with_twitter_and_github_not_working(self, twitter_api, git_hub_login, db):
        scenario = self.Scenario(twitter_api, git_hub_login, db=db)

        scenario.given_two_existing_developers()
        scenario.given_twitter_is_down()
        scenario.given_github_is_down()

        scenario.when_checking_if_the_developers_are_connected()

        scenario.then_the_response_status_code_is(200)

        scenario.when_parsing_the_response_data()

        scenario.then_the_db_will_not_store_anything()

        scenario.then_the_response_will_contain_one_error_for_each_service_and_user()

    class Scenario(HttpScenario, ExternalServicesScenario):
        TEST_DEV_NAME1 = 'test name 1'
        TEST_DEV_NAME2 = 'test name 2'

        TEST_SHARED_ORG_EXT_ID1 = 13
        TEST_SHARED_ORG_EXT_ID2 = 17
        TEST_SHARED_ORG_NAME1 = 'shared github org1'
        TEST_SHARED_ORG_NAME2 = 'shared github org2'
        TEST_SHARED_ORG_INTERNAL_ID1 = 29
        TEST_SHARED_ORG_INTERNAL_ID2 = 31

        TEST_UNIQUE_ORG_ID1 = 19
        TEST_UNIQUE_ORG_ID2 = 23
        TEST_UNIQUE_ORG_NAME1 = 'github org1 unique to one user'
        TEST_UNIQUE_ORG_NAME2 = 'github org2 unique to the other user'

        TEST_TWITTER_ERROR = 'twitter error'
        TEST_GITHUB_ERROR = 'error from github'

        def __init__(
                self, twitter_api_class=MagicMock(), git_hub_login=MagicMock(), db=MagicMock(),
                connection_db_class=MagicMock(), organization_db_class=MagicMock()
        ):
            HttpScenario.__init__(self)
            ExternalServicesScenario.__init__(self, twitter_api_class, git_hub_login)

            self.db = db
            self.connection_db_class = connection_db_class
            self.connection_obj = MagicMock()
            self.connection_db_class.return_value = self.connection_obj

            self.organization_db_class = organization_db_class
            self.existing_stored_organization = MagicMock()
            self.not_stored_organization_object = MagicMock()

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
            self.connection_obj.dev1 = self.TEST_DEV_NAME1
            self.connection_obj.dev2 = self.TEST_DEV_NAME2

        def given_they_follow_each_other_on_twitter(self):
            followers_list = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
            followers_list[0].name = self.dev1
            followers_list[1].name = 'another user 1'
            followers_list[2].name = self.dev2
            followers_list[3].name = 'another user 2'
            self.twitter_api.GetFollowers.return_value = followers_list
            self.connection_obj.are_linked = True

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

        def given_the_db_object_stores_the_developers_as_unconnected(self):
            self.connection_obj.are_linked = False
            self.connection_obj.organizations = []

        def given_the_db_object_stores_the_developers_as_connected_with_no_common_organizations(self):
            self.connection_db_class.query.filter_by.return_value = MagicMock()
            self.connection_db_class.query.filter_by.return_value.count.return_value = 0
            self.connection_obj.are_linked = True
            self.connection_obj.common_organizations = []

        def given_the_db_object_already_stored_only_one_of_the_shared_organizations(self):
            self.organization_db_class.query.filter_by.return_value.first.side_effect = [self.existing_stored_organization, None]
            self.organization_db_class.return_value = self.not_stored_organization_object

        def given_the_db_object_stores_the_developers_as_connected_with_their_shared_organizations(self):
            self.connection_obj.are_linked = True
            self.connection_obj.common_organizations = []

            self.existing_stored_organization.id = self.TEST_SHARED_ORG_INTERNAL_ID1
            self.not_stored_organization_object.id = self.TEST_SHARED_ORG_INTERNAL_ID2
            self.existing_stored_organization.name = self.TEST_SHARED_ORG_NAME1
            self.not_stored_organization_object.name = self.TEST_SHARED_ORG_NAME2

        def when_checking_if_the_developers_are_connected(self):
            self.response = self.client.get(f'/connected/realtime/{self.dev1}/{self.dev2}')

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

        def then_the_db_will_not_store_anything(self):
            self.db.session.add.assert_not_called()
            self.db.session.commit.assert_not_called()

        def then_the_result_will_be_saved_to_the_db_as_unconnected(self):
            self.connection_db_class.assert_called_with(
                dev1=self.TEST_DEV_NAME1, dev2=self.TEST_DEV_NAME2, are_linked=False
            )
            self.db.session.add.assert_called_once_with(self.connection_obj)
            self.db.session.commit.assert_called()

        def then_the_result_will_be_saved_to_the_db_as_connected(self):
            self.connection_db_class.assert_called_with(
                dev1=self.TEST_DEV_NAME1, dev2=self.TEST_DEV_NAME2, are_linked=True
            )
            self.db.session.add.assert_called_with(self.connection_obj)
            self.db.session.commit.assert_called()

        def then_the_db_will_be_queried_for_each_shared_organization(self):
            self.organization_db_class.query.filter_by.assert_has_calls = [
                call(external_id=self.TEST_SHARED_ORG_EXT_ID1),
                call(external_id=self.TEST_SHARED_ORG_EXT_ID2),
            ]

        def then_the_other_shared_organization_will_be_added_to_the_db(self):
            self.db.session.add.assert_any_call(self.not_stored_organization_object)
            self.db.session.commit.assert_called()

        def then_the_connection_object_will_contain_the_two_shared_organizations_db_object(self):
            assert self.connection_obj.common_organizations == [
                self.existing_stored_organization, self.not_stored_organization_object
            ]

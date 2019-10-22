import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest

from api import api
from connected.db_models import Connection, Organization
from tests.utils import HttpScenario, DbIntegrationScenario, ExternalServicesScenario


@pytest.mark.integration
class TestGetRegisteredConnection:

    def test_getting_the_connection_history_for_users_with_no_history(self):
        with self.Scenario() as scenario:
            scenario.given_two_existing_developers()

            scenario.when_getting_the_history_of_the_connection_between_the_developers()

            scenario.then_the_response_status_code_is(200)

            scenario.when_parsing_the_response_data()

            scenario.then_the_response_will_contain_an_empty_list()

    def test_getting_the_history_for_two_developers_found_to_not_be_connected(self):
        with self.Scenario() as scenario:
            scenario.given_two_existing_developers()
            scenario.given_the_users_were_not_connected()

            scenario.when_getting_the_history_of_the_connection_between_the_developers()

            scenario.then_the_response_status_code_is(200)

            scenario.when_parsing_the_response_data()

            scenario.then_the_response_will_contain_the_date_and_not_connected()

    def test_getting_the_history_for_two_developers_which_have_an_evolving_connection(self):
        with self.Scenario() as scenario:
            scenario.given_two_existing_developers()
            scenario.given_the_users_were_not_connected()
            scenario.given_the_users_are_linked_only_on_twitter()
            scenario.given_the_users_have_common_github_organizations()

            scenario.when_getting_the_history_of_the_connection_between_the_developers()

            scenario.then_the_response_status_code_is(200)

            scenario.when_parsing_the_response_data()

            scenario.then_the_response_will_contain_the_connection_history()

    class Scenario(HttpScenario, DbIntegrationScenario):
        TEST_DEV_NAME1 = 'test name 1'
        TEST_DEV_NAME2 = 'test name 2'

        TEST_SHARED_ORG_EXT_ID1 = 13
        TEST_SHARED_ORG_EXT_ID2 = 17
        TEST_SHARED_ORG_NAME1 = 'shared github org1'
        TEST_SHARED_ORG_NAME2 = 'shared github org2'

        CONNECTIONS_TIMESTAMPS = [
            datetime.utcnow() - timedelta(hours=5),
            datetime.utcnow() - timedelta(hours=4),
            datetime.utcnow() - timedelta(hours=3),
            datetime.utcnow() - timedelta(hours=2),
            datetime.utcnow() - timedelta(hours=1),
            datetime.utcnow(),
        ]

        def __init__(self):
            HttpScenario.__init__(self)
            DbIntegrationScenario.__init__(self)

            self.dev1 = None
            self.dev2 = None

            self.request = None

            api.testing = True

        def given_two_existing_developers(self):
            self.dev1 = self.TEST_DEV_NAME1
            self.dev2 = self.TEST_DEV_NAME2

        def given_the_users_were_not_connected(self):
            self.db.session.add(
                Connection(
                    dev1=self.TEST_DEV_NAME1, dev2=self.TEST_DEV_NAME2, are_linked=False,
                    timestamp=self.CONNECTIONS_TIMESTAMPS[2]
                )
            )
            self.db.session.commit()

        def given_the_users_are_linked_only_on_twitter(self):
            self.db.session.add(
                Connection(
                    dev1=self.TEST_DEV_NAME1, dev2=self.TEST_DEV_NAME2, are_linked=True,
                    timestamp=self.CONNECTIONS_TIMESTAMPS[3]
                )
            )
            self.db.session.commit()

        def given_the_users_have_common_github_organizations(self):
            org1 = Organization(external_id=self.TEST_SHARED_ORG_EXT_ID1, name=self.TEST_SHARED_ORG_NAME1)
            org2 = Organization(external_id=self.TEST_SHARED_ORG_EXT_ID2, name=self.TEST_SHARED_ORG_NAME2)
            self.db.session.add(org1)
            self.db.session.add(org2)
            self.db.session.commit()

            connection = Connection(
                dev1=self.TEST_DEV_NAME1, dev2=self.TEST_DEV_NAME2, are_linked=True,
                timestamp=self.CONNECTIONS_TIMESTAMPS[4]
            )
            connection.common_organizations.append(org1)
            connection.common_organizations.append(org2)
            self.db.session.add(connection)
            self.db.session.commit()

        def when_getting_the_history_of_the_connection_between_the_developers(self):
            self.response = self.client.get(f'/connected/register/{self.dev1}/{self.dev2}')

        def then_the_response_will_contain_an_empty_list(self):
            assert self.result_data == []

        def then_the_response_will_contain_the_date_and_not_connected(self):
            assert self.result_data[0]['connected'] == False
            assert self.result_data[0].get('registered_at', None) is not None

        def then_the_response_will_contain_the_connection_history(self):
            assert len(self.result_data) == 3

            assert self.result_data[0]['connected'] == False

            assert self.result_data[1]['connected'] == True
            assert not self.result_data[1]['organizations']

            assert self.result_data[2]['connected'] == True
            assert self.result_data[2]['organizations'] == [self.TEST_SHARED_ORG_NAME1, self.TEST_SHARED_ORG_NAME2]


class TestGetConnection:

    @patch('api.connected.services.login')
    @patch('api.connected.services.Api')
    def test_getting_the_connection_between_two_users_twice_in_a_row_will_only_store_it_once(
            self, twitter_api, git_hub_login
    ):
        with self.Scenario(twitter_api, git_hub_login) as scenario:
            scenario.given_two_existing_developers()
            scenario.given_they_don_t_follow_each_other_on_twitter()
            scenario.given_they_share_two_organizations_on_github()

            scenario.when_checking_if_the_developers_are_connected()
            scenario.then_the_response_status_code_is(200)
            time.sleep(0.1)
            scenario.when_checking_if_the_developers_are_connected()
            scenario.then_the_response_status_code_is(200)

            scenario.when_getting_the_history_of_the_connection_between_the_developers()
            scenario.then_the_response_status_code_is(200)

            scenario.when_parsing_the_response_data()

            scenario.then_the_response_will_contain_the_connection_history_with_only_one_entry()

    class Scenario(HttpScenario, DbIntegrationScenario, ExternalServicesScenario):
        TEST_DEV_NAME1 = 'test name 1'
        TEST_DEV_NAME2 = 'test name 2'

        TEST_SHARED_ORG_EXT_ID1 = 13
        TEST_SHARED_ORG_EXT_ID2 = 17
        TEST_SHARED_ORG_NAME1 = 'shared github org1'
        TEST_SHARED_ORG_NAME2 = 'shared github org2'

        def __init__(self, twitter_api_class=MagicMock(), git_hub_login=MagicMock()):
            HttpScenario.__init__(self)
            DbIntegrationScenario.__init__(self)
            ExternalServicesScenario.__init__(self, twitter_api_class, git_hub_login)

            self.dev1 = None
            self.dev2 = None

            self.request = None

            api.testing = True

        def given_two_existing_developers(self):
            self.dev1 = self.TEST_DEV_NAME1
            self.dev2 = self.TEST_DEV_NAME2

        def given_they_don_t_follow_each_other_on_twitter(self):
            self.twitter_api.GetFollowers.return_value = []

        def given_they_share_two_organizations_on_github(self):
            shared_orgs = [MagicMock(), MagicMock()]
            shared_orgs[0].id = self.TEST_SHARED_ORG_EXT_ID1
            shared_orgs[1].id = self.TEST_SHARED_ORG_EXT_ID2
            shared_orgs[0].login = self.TEST_SHARED_ORG_NAME1
            shared_orgs[1].login = self.TEST_SHARED_ORG_NAME2

            self.git_hub.organizations_with.return_value = shared_orgs

        def when_checking_if_the_developers_are_connected(self):
            self.response = self.client.get(f'/connected/realtime/{self.dev1}/{self.dev2}')

        def when_getting_the_history_of_the_connection_between_the_developers(self):
            self.response = self.client.get(f'/connected/register/{self.dev1}/{self.dev2}')

        def then_the_response_will_contain_the_connection_history_with_only_one_entry(self):
            assert len(self.result_data) == 1

            assert self.result_data[0]['connected'] == True
            assert self.result_data[0]['organizations'] == [self.TEST_SHARED_ORG_NAME1, self.TEST_SHARED_ORG_NAME2]

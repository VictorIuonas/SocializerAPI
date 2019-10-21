from typing import Callable, List, Tuple

from connected.exceptions import ExternalServiceException


class CreateConnectionDataUseCase:

    def __init__(self, twitter_service, github_service, connection_repo):
        self.twitter_service = twitter_service
        self.github_service = github_service
        self.connection_repo = connection_repo

    def execute(self, dev1: str, dev2: str):
        exceptions = []
        get_followers = lambda service, dev: service.get_followers(dev)
        get_organizations = lambda service, dev: service.get_organizations_for_user(dev)

        dev1_followers, exceptions = self.try_get_data(dev1, self.twitter_service, exceptions, get_followers)
        dev2_followers, exceptions = self.try_get_data(dev2, self.twitter_service, exceptions, get_followers)
        dev1_orgs, exceptions = self.try_get_data(dev1, self.github_service, exceptions, get_organizations)
        dev2_orgs, exceptions = self.try_get_data(dev2, self.github_service, exceptions, get_organizations)

        if not exceptions:
            common_orgs = list(set(dev1_orgs) & set(dev2_orgs))

            are_connected = (dev1 in dev2_followers and dev2 in dev1_followers) or (len(common_orgs) > 0)

            result = self.connection_repo.get_or_create_connection_between_developers(
                dev1, dev2, are_connected, common_organizations=common_orgs
            )

            return result, []
        else:
            return None, exceptions

    @staticmethod
    def try_get_data(
            dev: str, service, exception_list: List[ExternalServiceException],
            func_to_call: Callable[[object, str], List[str]]
    ) -> Tuple[List[str], List[ExternalServiceException]]:
        result = []
        try:
            result = func_to_call(service, dev)
        except ExternalServiceException as error:
            exception_list.append(error)

        return result, exception_list


class GetConnectionHistoryUseCase:

    def __init__(self, connection_repo):
        self.connection_repo = connection_repo

    def execute(self, dev1: str, dev2: str):
        return self.connection_repo.get_connection_for_developers(dev1, dev2), []

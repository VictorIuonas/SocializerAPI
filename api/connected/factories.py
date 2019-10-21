from api import api
from api.connected.use_cases import CreateConnectionDataUseCase, GetConnectionHistoryUseCase
from connected.repositories import ConnectionsRepository
from connected.services import TwitterService, GitHubService


def build_twitter_service() -> TwitterService:
    return TwitterService(config=api.config)


def build_github_service() -> GitHubService:
    return GitHubService(config=api.config)


def build_create_connection_data_use_case() -> CreateConnectionDataUseCase:
    return CreateConnectionDataUseCase(
        twitter_service=build_twitter_service(), github_service=build_github_service(),
        connection_repo=ConnectionsRepository()
    )


def build_get_connection_history_use_case() -> GetConnectionHistoryUseCase:
    return GetConnectionHistoryUseCase(ConnectionsRepository())

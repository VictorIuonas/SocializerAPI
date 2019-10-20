from api import api
from api.connected.use_cases import CreateConnectionDataUseCase
from connected.services import TwitterService, GitHubService


def build_twitter_service() -> TwitterService:
    return TwitterService(config=api.config)

def build_github_service() -> GitHubService:
    return GitHubService(config=api.config)


def build_create_connection_data_use_case() -> CreateConnectionDataUseCase:
    return CreateConnectionDataUseCase(twitter_service=build_twitter_service(), github_service=build_github_service())

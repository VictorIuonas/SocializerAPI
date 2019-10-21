import json
import os
from unittest.mock import MagicMock

from api import api, db
from config import basedir


class ExternalServicesScenario:
    def __init__(self, twitter_api_class, git_hub_login):
        self.twitter_api = MagicMock()
        self.twitter_api_class = twitter_api_class
        self.twitter_api_class.return_value = self.twitter_api

        self.git_hub_login = git_hub_login
        self.git_hub = MagicMock()
        self.git_hub_login.return_value = self.git_hub


class HttpScenario:
    def __init__(self):
        self.client = api.test_client()

        self.response = None
        self.result_data = None

    def when_parsing_the_response_data(self):
        self.result_data = json.loads(self.response.data)

    def then_the_response_status_code_is(self, status_code: int):
        assert self.response.status_code == status_code


class DbIntegrationScenario:
    def __init__(self):
        api.config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.db = db

    def __enter__(self):
        self.clean_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def clean_db(self):
        self.db.drop_all()
        self.db.create_all()

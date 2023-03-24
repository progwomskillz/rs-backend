from datetime import datetime

from application.structure import structure
from data.translators.polls import PollTranslator
from data.translators.users import UserTranslator
from domain.entities.polls import Poll
from domain.entities.revise_requests import ReviseRequest
from domain.entities.users import User
from domain.utils import constants
from tests.factories.revise_requests import ReviseRequestFactory


class TestReviseRequestTranslator():
    def setup_method(self):
        self.translator = structure.revise_request_translator

    def test_init(self):
        assert isinstance(
            self.translator.user_translator,
            UserTranslator
        ) is True
        assert isinstance(
            self.translator.poll_translator,
            PollTranslator
        ) is True

    def test_from_document(self):
        document = {
            "_id": "test_id",
            "user": {
                "_id": "test_id",
                "role": constants.user_roles.public_official,
                "username": "test_username",
                "password_hash": b"test_password_hash",
                "tokens_pairs": [
                    {"access": "test_access", "refresh": "test_refresh"}
                ],
                "profile": {
                    "first_name": "test_first_name",
                    "last_name": "test_last_name"
                }
            },
            "poll": {
            "_id": "test_id",
                "user": {
                    "_id": "test_id",
                    "role": constants.user_roles.community_social_worker,
                    "username": "test_username",
                    "password_hash": b"test_password_hash",
                    "tokens_pairs": [
                        {"access": "test_access", "refresh": "test_refresh"}
                    ],
                    "profile": {
                        "first_name": "test_first_name",
                        "last_name": "test_last_name"
                    }
                },
                "updated_at": datetime.utcnow(),
                "community_name": "test_community_name",
                "community_size": 50,
                "feedbacks": [
                    {"bothers": "test_bothers", "age": 25}
                ],
                "summary": [
                    {"title": "test_title", "count": 1, "percentage": 100}
                ]
            }
        }

        result = self.translator.from_document(document)

        assert isinstance(result, ReviseRequest) is True
        assert result.id == document["_id"]
        assert isinstance(result.user, User) is True
        assert result.user.id == document["user"]["_id"]
        assert isinstance(result.poll, Poll) is True
        assert result.poll.id == document["poll"]["_id"]

    def test_to_document(self):
        revise_request = ReviseRequestFactory.generic()

        result = self.translator.to_document(revise_request)

        assert result == {
            "_id": None,
            "user_id": None,
            "poll_id": None
        }

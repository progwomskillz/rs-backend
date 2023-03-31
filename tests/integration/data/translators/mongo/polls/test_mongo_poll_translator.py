from datetime import datetime

from application.structure import structure
from data.translators.mongo.polls import MongoFeedbackTranslator, MongoStatsTranslator
from data.translators.mongo.users import MongoUserTranslator
from domain.entities.polls import Feedback, Poll, Stats
from domain.entities.users import CommunitySocialWorkerProfile, User
from domain.utils import constants
from tests.factories.polls import PollFactory


class TestMongoPollTranslator():
    def setup_method(self):
        self.translator = structure.mongo_poll_translator

    def test_init(self):
        assert isinstance(
            self.translator.user_translator,
            MongoUserTranslator
        ) is True
        assert isinstance(
            self.translator.feedback_translator,
            MongoFeedbackTranslator
        ) is True
        assert isinstance(
            self.translator.stats_translator,
            MongoStatsTranslator
        ) is True

    def test_from_document(self):
        document = {
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

        result = self.translator.from_document(document)

        assert isinstance(result, Poll) is True
        assert result.id == document["_id"]
        assert isinstance(result.user, User) is True
        assert result.user.id == document["user"]["_id"]
        assert result.user.role == document["user"]["role"]
        assert result.user.username == document["user"]["username"]
        assert result.user.password_hash == document["user"]["password_hash"]
        assert isinstance(result.user.tokens_pairs, list) is True
        assert len(result.user.tokens_pairs) ==\
            len(document["user"]["tokens_pairs"])
        for i, tokens_pair in enumerate(result.user.tokens_pairs):
            assert tokens_pair.access ==\
                document["user"]["tokens_pairs"][i]["access"]
            assert tokens_pair.refresh ==\
                document["user"]["tokens_pairs"][i]["refresh"]
        assert isinstance(
            result.user.profile,
            CommunitySocialWorkerProfile
        ) is True
        assert result.user.profile.first_name ==\
            document["user"]["profile"]["first_name"]
        assert result.user.profile.last_name ==\
            document["user"]["profile"]["last_name"]
        assert result.updated_at == document["updated_at"]
        assert result.community_name == document["community_name"]
        assert result.community_size == document["community_size"]
        assert isinstance(result.feedbacks, list) is True
        assert len(result.feedbacks) == len(document["feedbacks"])
        for i, feedback in enumerate(result.feedbacks):
            assert isinstance(feedback, Feedback) is True
            assert feedback.bothers == document["feedbacks"][i]["bothers"]
            assert feedback.age == document["feedbacks"][i]["age"]
        assert isinstance(result.summary, list) is True
        assert len(result.summary) == len(document["summary"])
        for i, stats in enumerate(result.summary):
            assert isinstance(stats, Stats) is True
            assert stats.title == document["summary"][i]["title"]
            assert stats.count == document["summary"][i]["count"]
            assert stats.percentage == document["summary"][i]["percentage"]

    def test_to_document(self):
        poll = PollFactory.generic()

        result = self.translator.to_document(poll)

        assert result == {
            "_id": None,
            "user_id": None,
            "updated_at": poll.updated_at,
            "community_name": poll.community_name,
            "community_size": poll.community_size,
            "feedbacks": [
                {"bothers": feedback.bothers, "age": feedback.age}
                for feedback in poll.feedbacks
            ]
        }

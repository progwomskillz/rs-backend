from datetime import datetime

from mock import Mock

from data.translators.mongo.polls import MongoPollTranslator
from domain.entities.polls import Poll
from tests.factories.polls import FeedbackFactory, PollFactory, StatsFactory
from tests.factories.users import UserFactory


class TestMongoPollTranslator():
    def setup_method(self):
        self.user_translator_mock = Mock()
        self.feedback_translator_mock = Mock()
        self.stats_translator_mock = Mock()

        self.translator = MongoPollTranslator(
            self.user_translator_mock,
            self.feedback_translator_mock,
            self.stats_translator_mock
        )

    def test_init(self):
        assert self.translator.user_translator == self.user_translator_mock
        assert self.translator.feedback_translator ==\
            self.feedback_translator_mock
        assert self.translator.stats_translator == self.stats_translator_mock

    def test_from_document(self):
        user_document = {"_id": "test_id"}
        feedbacks_documents = [
            {"bothers": f"test_bothers_{i}", "age": 18 + i}
            for i in range(10)
        ]
        summary_documents = [
            {"title": f"test_title_{i}", "count": 10 + i, "percentage": 30 + i}
            for i in range(3)
        ]
        document = {
            "_id": "test_id",
            "user": user_document,
            "updated_at": datetime.utcnow(),
            "community_name": "test_community_name",
            "community_size": "test_community_size",
            "feedbacks": feedbacks_documents,
            "summary": summary_documents
        }

        user = UserFactory.community_social_worker()
        self.user_translator_mock.from_document.return_value = user
        feedbacks = [
            FeedbackFactory.generic()
            for _ in range(len(feedbacks_documents))
        ]
        self.feedback_translator_mock.from_document.side_effect = feedbacks
        summary = [
            StatsFactory.generic()
            for _ in range(len(summary_documents))
        ]
        self.stats_translator_mock.from_document.side_effect = summary

        result = self.translator.from_document(document)

        assert isinstance(result, Poll) is True
        assert result.id == document["_id"]
        assert result.user == user
        assert result.updated_at == document["updated_at"]
        assert result.community_name == document["community_name"]
        assert result.community_size == document["community_size"]
        assert result.feedbacks == feedbacks
        assert result.summary == summary
        self.user_translator_mock.from_document.assert_called_once_with(
            user_document
        )
        assert self.feedback_translator_mock.from_document.call_count ==\
            len(feedbacks_documents)
        for feedback_document in feedbacks_documents:
            self.feedback_translator_mock.from_document.assert_any_call(
                feedback_document
            )
        assert self.stats_translator_mock.from_document.call_count ==\
            len(summary_documents)
        for stats_document in summary_documents:
            self.stats_translator_mock.from_document.assert_any_call(
                stats_document
            )

    def test_to_document(self):
        poll = PollFactory.generic()

        feedbacks_documents_mock = [
            {"bothers": f"test_bothers_{i}", "age": 18 + i}
            for i in range(len(poll.feedbacks))
        ]
        self.feedback_translator_mock.to_document.side_effect =\
            feedbacks_documents_mock

        result = self.translator.to_document(poll)

        assert result == {
            "_id": None,
            "user_id": None,
            "updated_at": poll.updated_at,
            "community_name": poll.community_name,
            "community_size": poll.community_size,
            "feedbacks": feedbacks_documents_mock
        }
        self.user_translator_mock.to_document.assert_not_called()
        assert self.feedback_translator_mock.to_document.call_count ==\
            len(poll.feedbacks)
        for feedback in poll.feedbacks:
            self.feedback_translator_mock.to_document.assert_any_call(
                feedback
            )
        self.stats_translator_mock.to_document.assert_not_called()

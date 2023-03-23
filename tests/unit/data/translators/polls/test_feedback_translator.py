from data.translators.polls import FeedbackTranslator
from domain.entities.polls import Feedback
from tests.factories.polls import FeedbackFactory


class TestFeedbackTranslator():
    def setup_method(self):
        self.translator = FeedbackTranslator()

    def test_from_document(self):
        document = {"bothers": "test_bothers", "age": 24}

        result = self.translator.from_document(document)

        assert isinstance(result, Feedback) is True
        assert result.bothers == document["bothers"]
        assert result.age == document["age"]

    def test_to_document(self):
        feedback = FeedbackFactory.generic()

        result = self.translator.to_document(feedback)

        assert result == {
            "bothers": feedback.bothers,
            "age": feedback.age
        }

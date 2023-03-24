from mock import Mock

from data.translators.revise_requests import ReviseRequestTranslator
from domain.entities.revise_requests import ReviseRequest
from tests.factories.revise_requests import ReviseRequestFactory


class TestReviseRequestTranslator():
    def setup_method(self):
        self.user_translator_mock = Mock()
        self.poll_translator_mock = Mock()

        self.translator = ReviseRequestTranslator(
            self.user_translator_mock,
            self.poll_translator_mock
        )

    def test_init(self):
        assert self.translator.user_translator == self.user_translator_mock
        assert self.translator.poll_translator == self.poll_translator_mock

    def test_from_document(self):
        user_document = {"_id": "test_id"}
        poll_document = {"_id": "test_id"}
        document = {
            "_id": "test_id",
            "user": user_document,
            "poll": poll_document
        }

        user_mock = Mock()
        self.user_translator_mock.from_document.return_value = user_mock
        poll_mock = Mock()
        self.poll_translator_mock.from_document.return_value = poll_mock

        result = self.translator.from_document(document)

        assert isinstance(result, ReviseRequest) is True
        assert result.id == document["_id"]
        assert result.user == user_mock
        assert result.poll == poll_mock
        self.user_translator_mock.from_document.assert_called_once_with(
            user_document
        )
        self.poll_translator_mock.from_document.assert_called_once_with(
            poll_document
        )

    def test_to_document(self):
        revise_request = ReviseRequestFactory.generic()

        result = self.translator.to_document(revise_request)

        assert result == {
            "_id": None,
            "user_id": None,
            "poll_id": None
        }
        self.user_translator_mock.to_document.assert_not_called()
        self.poll_translator_mock.to_document.assert_not_called()

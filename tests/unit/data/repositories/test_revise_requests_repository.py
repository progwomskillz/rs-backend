from mock import Mock, patch

from .utils import RepositoryTestsConfigurator
from data.repositories import ReviseRequestsRepository
from data.utils import constants
from domain.entities.shared import Page
from tests.factories.revise_requests import ReviseRequestFactory


class TestReviseRequestsRepository(RepositoryTestsConfigurator):
    def setup_method(self):
        self.init()

    @patch("data.repositories.base_repository.pymongo")
    def init(self, pymongo_mock):
        self.configure_mocks(pymongo_mock)

        self.repository = ReviseRequestsRepository(
            self.scheme,
            self.username,
            self.password,
            self.host,
            self.port,
            self.db_name,
            self.collection_name,
            self.translator_mock
        )

    def test_get_page_not_found(self):
        poll_user_id = None
        page = 1
        page_size = 10

        docs_cursor_mock = []
        count_cursor_mock = [{"count": 0}]
        self.collection_mock.aggregate.side_effect = [
            docs_cursor_mock,
            count_cursor_mock
        ]

        result = self.repository.get_page(poll_user_id, page, page_size)

        assert isinstance(result, Page) is True
        assert result.items == []
        assert result.page == page
        assert result.page_count == 1
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.revise_requests.default,
            {"$match": {"poll.user._id": None}},
            {"$skip": (page - 1) * page_size},
            {"$limit": page_size}
        ])
        self.translator_mock.from_document.assert_not_called()
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.revise_requests.default,
            {"$match": {"poll.user._id": None}},
            {"$count": "count"}
        ])
        assert self.collection_mock.aggregate.call_count == 2

    def test_get_page(self):
        poll_user_id = "test_poll_user_id"
        page = 2
        page_size = 10

        document_mock = Mock()
        docs_cursor_mock = [document_mock]
        count_cursor_mock = [{"count": 11}]
        self.collection_mock.aggregate.side_effect = [
            docs_cursor_mock,
            count_cursor_mock
        ]

        revise_request = ReviseRequestFactory.generic()
        self.translator_mock.from_document.return_value = revise_request

        result = self.repository.get_page(poll_user_id, page, page_size)

        assert isinstance(result, Page) is True
        assert result.items == [revise_request]
        assert result.page == page
        assert result.page_count == 2
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.revise_requests.default,
            {"$match": {"poll.user._id": None}},
            {"$skip": (page - 1) * page_size},
            {"$limit": page_size}
        ])
        self.translator_mock.from_document.assert_called_once_with(
            document_mock
        )
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.revise_requests.default,
            {"$match": {"poll.user._id": None}},
            {"$count": "count"}
        ])
        assert self.collection_mock.aggregate.call_count == 2

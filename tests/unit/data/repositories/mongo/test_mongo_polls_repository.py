from mock import Mock, patch

from .utils import RepositoryTestsConfigurator
from data.repositories.mongo import MongoPollsRepository
from data.utils import constants
from domain.entities.shared import Page
from tests.factories.polls import PollFactory


class TestMongoPollsRepository(RepositoryTestsConfigurator):
    def setup_method(self):
        self.init()

    @patch("data.repositories.mongo.mongo_base_repository.pymongo")
    def init(self, pymongo_mock):
        self.configure_mocks(pymongo_mock)
        self.stats_translator_mock = Mock()

        self.repository = MongoPollsRepository(
            self.scheme,
            self.username,
            self.password,
            self.host,
            self.port,
            self.db_name,
            self.collection_name,
            self.translator_mock,
            self.stats_translator_mock
        )

    def test_get_page_not_found(self):
        user_id = None
        page = 1
        page_size = 10

        docs_cursor_mock = []
        count_cursor_mock = [{"count": 0}]
        self.collection_mock.aggregate.side_effect = [
            docs_cursor_mock,
            count_cursor_mock
        ]

        result = self.repository.get_page(user_id, page, page_size)

        assert isinstance(result, Page) is True
        assert result.items == []
        assert result.page == page
        assert result.page_count == 1
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.polls.default,
            {"$skip": (page - 1) * page_size},
            {"$limit": page_size}
        ])
        self.translator_mock.from_document.assert_not_called()
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.polls.default,
            {"$count": "count"}
        ])
        assert self.collection_mock.aggregate.call_count == 2

    def test_get_page(self):
        user_id = "test_user_id"
        page = 2
        page_size = 10

        document_mock = Mock()
        docs_cursor_mock = [document_mock]
        count_cursor_mock = [{"count": 11}]
        self.collection_mock.aggregate.side_effect = [
            docs_cursor_mock,
            count_cursor_mock
        ]

        poll = PollFactory.generic()
        self.translator_mock.from_document.return_value = poll

        result = self.repository.get_page(user_id, page, page_size)

        assert isinstance(result, Page) is True
        assert result.items == [poll]
        assert result.page == page
        assert result.page_count == 2
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.polls.default,
            {"$match": {"user._id": None}},
            {"$skip": (page - 1) * page_size},
            {"$limit": page_size}
        ])
        self.translator_mock.from_document.assert_called_once_with(
            document_mock
        )
        self.collection_mock.aggregate.assert_any_call([
            {"$sort": {"_id": -1}},
            *constants.pipelines.polls.default,
            {"$match": {"user._id": None}},
            {"$count": "count"}
        ])
        assert self.collection_mock.aggregate.call_count == 2

    def test_get_summary_empty(self):
        self.collection_mock.aggregate.return_value = []

        result = self.repository.get_summary()

        assert result == []
        self.collection_mock.aggregate.assert_called_once_with([
            {
                "$unwind": {
                    "path": "$feedbacks"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "feedbacks": {
                        "$push": "$feedbacks"
                    }
                }
            },
            *constants.pipelines.polls.calc_summary
        ])
        self.stats_translator_mock.from_document.assert_not_called()

    def test_get_summary(self):
        stats_mock = Mock()
        self.collection_mock.aggregate.return_value = [
            {"summary": [stats_mock]}
        ]
        translated_stats_mock = Mock()
        self.stats_translator_mock.from_document.return_value =\
            translated_stats_mock

        result = self.repository.get_summary()

        assert result == [translated_stats_mock]
        self.collection_mock.aggregate.assert_called_once_with([
            {
                "$unwind": {
                    "path": "$feedbacks"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "feedbacks": {
                        "$push": "$feedbacks"
                    }
                }
            },
            *constants.pipelines.polls.calc_summary
        ])
        self.stats_translator_mock.from_document.assert_called_once_with(
            stats_mock
        )

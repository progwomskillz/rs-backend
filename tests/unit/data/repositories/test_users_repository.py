from mock import Mock, patch

from .utils import RepositoryTestsConfigurator
from data.repositories import UsersRepository
from domain.entities.shared import Page
from tests.factories.users import UserFactory


class TestUsersRepository(RepositoryTestsConfigurator):
    def setup_method(self):
        self.init()

    @patch("data.repositories.base_repository.pymongo")
    def init(self, pymongo_mock):
        self.configure_mocks(pymongo_mock)

        self.repository = UsersRepository(
            self.scheme,
            self.username,
            self.password,
            self.host,
            self.port,
            self.db_name,
            self.collection_name,
            self.translator_mock
        )

    def test_find_by_username_not_found(self):
        username = "test_username"

        cursor_mock = []
        self.collection_mock.aggregate.return_value = cursor_mock

        result = self.repository.find_by_username(username)

        assert result is None
        self.collection_mock.aggregate.assert_called_once_with([
            {
                "$match": {
                    "username": username
                }
            },
            {"$limit": 1}
        ])
        self.translator_mock.from_document.assert_not_called()

    def test_find_by_username(self):
        username = "test_username"

        document_mock = Mock()
        cursor_mock = [document_mock]
        self.collection_mock.aggregate.return_value = cursor_mock

        user = UserFactory.admin()
        self.translator_mock.from_document.return_value = user

        result = self.repository.find_by_username(username)

        assert result == user
        self.collection_mock.aggregate.assert_called_once_with([
            {
                "$match": {
                    "username": username
                }
            },
            {"$limit": 1}
        ])
        self.translator_mock.from_document.assert_called_once_with(
            document_mock
        )

    def test_get_page_by_role_not_found(self):
        role = "test_role"
        page = 1
        page_size = 10

        docs_cursor_mock = []
        count_cursor_mock = [{"count": 0}]
        self.collection_mock.aggregate.side_effect = [
            docs_cursor_mock,
            count_cursor_mock
        ]

        result = self.repository.get_page_by_role(role, page, page_size)

        assert isinstance(result, Page) is True
        assert result.items == []
        assert result.page == page
        assert result.page_count == 1
        self.collection_mock.aggregate.assert_any_call([
            {"$match": {"role": role}},
            {"$skip": (page - 1) * page_size},
            {"$limit": page_size}
        ])
        self.translator_mock.from_document.assert_not_called()
        self.collection_mock.aggregate.assert_any_call([
            {"$match": {"role": role}},
            {"$count": "count"}
        ])
        assert self.collection_mock.aggregate.call_count == 2

    def test_get_page_by_role(self):
        role = "test_role"
        page = 2
        page_size = 10

        document_mock = Mock()
        docs_cursor_mock = [document_mock]
        count_cursor_mock = [{"count": 11}]
        self.collection_mock.aggregate.side_effect = [
            docs_cursor_mock,
            count_cursor_mock
        ]

        user = UserFactory.admin()
        self.translator_mock.from_document.return_value = user

        result = self.repository.get_page_by_role(role, page, page_size)

        assert isinstance(result, Page) is True
        assert result.items == [user]
        assert result.page == page
        assert result.page_count == 2
        self.collection_mock.aggregate.assert_any_call([
            {"$match": {"role": role}},
            {"$skip": (page - 1) * page_size},
            {"$limit": page_size}
        ])
        self.translator_mock.from_document.assert_called_once_with(
            document_mock
        )
        self.collection_mock.aggregate.assert_any_call([
            {"$match": {"role": role}},
            {"$count": "count"}
        ])
        assert self.collection_mock.aggregate.call_count == 2

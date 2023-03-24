from mock import Mock, MagicMock, patch

from .utils import RepositoryTestsConfigurator
from data.repositories.base_repository import BaseRepository


class BaseModel():
    def __init__(self, id):
        self.id = id


class TestBaseRepository(RepositoryTestsConfigurator):
    def setup_method(self):
        self.init()

    @patch("data.repositories.base_repository.pymongo")
    def init(self, pymongo_mock):
        self.pymongo_mock = pymongo_mock
        self.configure_mocks(pymongo_mock)

        self.repository = BaseRepository(
            self.scheme,
            self.username,
            self.password,
            self.host,
            self.port,
            self.db_name,
            self.collection_name,
            self.translator_mock
        )

    def test_init(self):
        self.pymongo_mock.MongoClient.assert_called_once_with(
            f"{self.scheme}://{self.username}:{self.password}@{self.host}:{self.port}"
        )
        self.client_mock.__getitem__.assert_called_once_with(self.db_name)
        self.db_mock.__getitem__.assert_called_once_with(self.collection_name)
        assert self.repository.collection == self.collection_mock
        assert self.repository.translator == self.translator_mock

    def test_del(self):
        del self.repository

        self.client_mock.close.assert_called_once()

    @patch("data.repositories.base_repository.ObjectId")
    def test_find_by_id_invalid(self, ObjectId_mock):
        ObjectId_mock.is_valid.return_value = False

        id = "test_id"

        result = self.repository.find_by_id(id)

        assert result is None
        ObjectId_mock.is_valid.assert_called_once_with(id)
        ObjectId_mock.assert_not_called()
        self.collection_mock.aggregate.assert_not_called()
        self.translator_mock.from_document.assert_not_called()

    @patch("data.repositories.base_repository.ObjectId")
    def test_find_by_id_not_found(self, ObjectId_mock):
        ObjectId_mock.is_valid.return_value = True
        id_mock = Mock()
        ObjectId_mock.return_value = id_mock
        self.collection_mock.aggregate.return_value = []

        id = "test_id"

        result = self.repository.find_by_id(id)

        assert result is None
        ObjectId_mock.is_valid.assert_called_once_with(id)
        ObjectId_mock.assert_called_once_with(id)
        self.collection_mock.aggregate.assert_called_once_with([
            {"$sort": {"_id": -1}},
            {"$match": {"_id": id_mock}},
            {"$limit": 1}
        ])
        self.translator_mock.from_document.assert_not_called()

    @patch("data.repositories.base_repository.ObjectId")
    def test_find_by_id(self, ObjectId_mock):
        ObjectId_mock.is_valid.return_value = True
        id_mock = Mock()
        ObjectId_mock.return_value = id_mock
        document_mock = Mock()
        self.collection_mock.aggregate.return_value = [document_mock]
        translated_mock = Mock()
        self.translator_mock.from_document.return_value = translated_mock

        id = "test_id"

        result = self.repository.find_by_id(id)

        assert result == translated_mock
        ObjectId_mock.is_valid.assert_called_once_with(id)
        ObjectId_mock.assert_called_once_with(id)
        self.collection_mock.aggregate.assert_called_once_with([
            {"$sort": {"_id": -1}},
            {"$match": {"_id": id_mock}},
            {"$limit": 1}
        ])
        self.translator_mock.from_document.assert_called_once_with(
            document_mock
        )

    def test_update(self):
        model = BaseModel("test_id")

        document_mock = MagicMock()
        self.translator_mock.to_document.return_value = document_mock

        self.repository.update(model)

        self.translator_mock.to_document.assert_called_once_with(model)
        self.collection_mock.update_one.assert_called_once_with(
            {"_id": document_mock["_id"]},
            {"$set": document_mock}
        )

    @patch("data.repositories.base_repository.ObjectId")
    def test_delete(self, ObjectId_mock):
        id_mock = Mock()
        ObjectId_mock.return_value = id_mock

        model_mock = Mock()
        id = "test_id"
        model_mock.id = id

        self.repository.delete(model_mock)

        ObjectId_mock.assert_called_once_with(id)
        self.collection_mock.aggregate.delete_one({"_id": id_mock})

    def test_create(self):
        model = BaseModel("test_id")

        document_mock = Mock()
        self.translator_mock.to_document.return_value = document_mock
        cursor_mock = Mock()
        cursor_mock.inserted_id = "test_inserted_id"
        self.collection_mock.insert_one.return_value = cursor_mock

        result = self.repository.create(model)

        assert result == cursor_mock.inserted_id
        self.translator_mock.to_document.assert_called_once_with(model)
        document_mock.pop.assert_called_once_with("_id")
        self.collection_mock.insert_one.assert_called_once_with(document_mock)

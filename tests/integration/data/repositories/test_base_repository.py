import os

from bson import ObjectId
from pymongo.collection import Collection

from data.repositories.base_repository import BaseRepository


class BaseModel():
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


class BaseTranslator():
    def from_document(self, document):
        return BaseModel(
            str(document.get("_id")),
            document.get("name")
        )

    def to_document(self, model):
        return {
            "_id": ObjectId(model.id) if ObjectId.is_valid(model.id) else None,
            "name": model.name
        }


class TestBaseRepository():
    def setup_method(self):
        self.scheme = os.environ["DB_SCHEME"]
        self.username = os.environ["DB_USERNAME"]
        self.password = os.environ["DB_PASSWORD"]
        self.host = os.environ["DB_HOST"]
        self.port = os.environ["DB_PORT"]
        self.db_name = os.environ["DB_NAME"]
        self.collection_name = "base_collection"
        self.translator = BaseTranslator()

        self.repository = BaseRepository(
            self.scheme,
            self.username,
            self.password,
            self.host,
            self.port,
            self.db_name,
            self.collection_name,
            self.translator
        )

    def teardown_method(self):
        self.repository.collection.delete_many({})

    def create_and_save(self):
        model = BaseModel(None, "name")
        inserted_id = self.repository.create(model)

        document = self.translator.to_document(model)
        return self.repository.translator.from_document(
            {**document, "_id": inserted_id}
        )

    def test_init(self):
        assert isinstance(self.repository.collection, Collection) is True
        assert self.repository.collection.name == self.collection_name
        assert isinstance(self.repository.translator, BaseTranslator) is True

    def test_update(self):
        model = self.create_and_save()
        name = "new_name"
        model.set_name(name)

        self.repository.update(model)

        result = self.repository.find_by_id(model.id)

        assert result.name == name

    def test_create(self):
        name = "name"
        model = BaseModel(None, name)

        inserted_id = self.repository.create(model)

        result = self.repository.find_by_id(inserted_id)

        assert result is not None
        assert result.id == inserted_id

    def test_find_by_id_invalid_id(self):
        result = self.repository.find_by_id(123)

        assert result is None

    def test_find_by_id_not_found(self):
        result = self.repository.find_by_id("123456789012345678901234")

        assert result is None

    def test_find_by_id(self):
        model = self.create_and_save()

        result = self.repository.find_by_id(model.id)

        assert isinstance(model, BaseModel) is True
        assert result.id == model.id

    def test_find_by_id_none(self):
        model = self.create_and_save()

        self.repository.delete(model)

        result = self.repository.find_by_id(model.id)

        assert result is None

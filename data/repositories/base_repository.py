import math

import pymongo
from bson import ObjectId

from domain.entities.shared import Page


class BaseRepository():
    def __init__(
        self, scheme, username, password, host, port, db_name, collection_name,
        translator, default_pipeline=None
    ):
        credentials = ""
        if username:
            credentials = f"{username}:{password}@"
        connection_url = f"{scheme}://{credentials}{host}:{port}"
        self.__client = pymongo.MongoClient(connection_url)
        self.collection = self.__client[db_name][collection_name]
        self.translator = translator
        self.default_pipeline = default_pipeline if default_pipeline else []

    def __del__(self):
        self.__client.close()

    def find_by_id(self, id):
        id = self._to_object_id(id)
        if not id:
            return None
        pipeline = [{"$match": {"_id": id}}]
        return self._find(pipeline)

    def update(self, model):
        document = self.translator.to_document(model)
        self.collection.update_one({"_id": document["_id"]}, {"$set": document})

    def delete(self, model):
        self.collection.delete_one({"_id": self._to_object_id(model.id)})

    def create(self, model):
        document = self.translator.to_document(model)
        document.pop("_id")
        return str(self.collection.insert_one(document).inserted_id)

    def _find(self, pipeline):
        result = self._get(pipeline + [{"$limit": 1}])
        if not result:
            return None
        return result[0]

    def _get(self, pipeline):
        pipeline = self.default_pipeline + pipeline
        cursor = self.collection.aggregate(pipeline)
        result = [
            self.translator.from_document(document)
            for document in cursor
        ]
        return result

    def _get_page(self, pipeline, page, page_size):
        pipeline = self.default_pipeline + pipeline
        search_pipeline = [
            *pipeline,
            {"$skip": (page - 1) * page_size},
            {"$limit": page_size}
        ]
        documents_cursor = self.collection.aggregate(search_pipeline)
        items = [
            self.translator.from_document(document)
            for document in documents_cursor
        ]
        count = 0
        count_cursor = list(self.collection.aggregate([
            *pipeline,
            {"$count": "count"}]
        ))
        if count_cursor:
            count = count_cursor[0].get("count", 0)
        page_count = math.ceil(count / page_size)
        if page_count == 0:
            page_count = 1
        return Page(items, page, page_count)

    def _to_object_id(self, id):
        if not ObjectId.is_valid(id):
            return None
        return ObjectId(id)

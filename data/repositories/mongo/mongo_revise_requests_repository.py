from .mongo_base_repository import MongoBaseRepository
from data.utils import constants


class MongoReviseRequestsRepository(MongoBaseRepository):
    def __init__(
        self, scheme, username, password, host, port, db_name, collection_name,
        translator
    ):
        super().__init__(
            scheme, username, password, host, port, db_name, collection_name,
            translator, constants.pipelines.revise_requests.default
        )

    def get_page(self, poll_user_id, page, page_size):
        pipeline = [
            {"$match": {"poll.user._id": self._to_object_id(poll_user_id)}}
        ]
        return self._get_page(pipeline, page, page_size)

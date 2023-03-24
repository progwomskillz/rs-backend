from .base_repository import BaseRepository
from data.utils import constants


class PollsRepository(BaseRepository):
    def __init__(
        self, scheme, username, password, host, port, db_name, collection_name,
        translator, stats_translator
    ):
        super().__init__(
            scheme, username, password, host, port, db_name, collection_name,
            translator, constants.pipelines.polls.default
        )
        self.stats_translator = stats_translator

    def get_page(self, user_id, page, page_size):
        pipeline = []
        if user_id:
            pipeline.append(
                {"$match": {"user._id": self._to_object_id(user_id)}}
            )
        return self._get_page(pipeline, page, page_size)

    def get_summary(self):
        cursor = list(self.collection.aggregate([
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
        ]))
        if not cursor:
            return []
        return [
            self.stats_translator.from_document(stats)
            for stats in cursor[0].get("summary", [])
        ]

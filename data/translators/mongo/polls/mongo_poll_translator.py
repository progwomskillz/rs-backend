from bson import ObjectId

from domain.entities.polls import Poll


class MongoPollTranslator():
    def __init__(self, user_translator, feedback_translator, stats_translator):
        self.user_translator = user_translator
        self.feedback_translator = feedback_translator
        self.stats_translator = stats_translator

    def from_document(self, document):
        return Poll(
            str(document.get("_id")),
            self.user_translator.from_document(document.get("user")),
            document.get("updated_at"),
            document.get("community_name"),
            document.get("community_size"),
            [
                self.feedback_translator.from_document(feedback_document)
                for feedback_document in document.get("feedbacks", [])
            ],
            [
                self.stats_translator.from_document(stats_document)
                for stats_document in document.get("summary", [])
            ]
        )

    def to_document(self, poll):
        return {
            "_id": ObjectId(poll.id) if ObjectId.is_valid(poll.id) else None,
            "user_id": ObjectId(poll.user.id) if ObjectId.is_valid(poll.user.id) else None,
            "updated_at": poll.updated_at,
            "community_name": poll.community_name,
            "community_size": poll.community_size,
            "feedbacks": [
                self.feedback_translator.to_document(feedback)
                for feedback in poll.feedbacks
            ]
        }

from bson import ObjectId

from domain.entities.revise_requests import ReviseRequest


class ReviseRequestTranslator():
    def __init__(self, user_translator, poll_translator):
        self.user_translator = user_translator
        self.poll_translator = poll_translator

    def from_document(self, document):
        return ReviseRequest(
            str(document.get("_id")),
            self.user_translator.from_document(document.get("user")),
            self.poll_translator.from_document(document.get("poll"))
        )

    def to_document(self, revise_request):
        return {
            "_id": ObjectId(revise_request.id) if ObjectId.is_valid(revise_request.id) else None,
            "user_id": ObjectId(revise_request.user.id) if ObjectId.is_valid(revise_request.user.id) else None,
            "poll_id": ObjectId(revise_request.poll.id) if ObjectId.is_valid(revise_request.poll.id) else None
        }

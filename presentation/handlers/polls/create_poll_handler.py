from ..auth_base_handler import AuthBaseHandler
from domain.entities.polls.requests import CreatePollRequest
from domain.entities.polls import Feedback


class CreatePollHandler(AuthBaseHandler):
    def execute(self, request):
        feedbacks = request.json.get("feedbacks")
        if not isinstance(feedbacks, list):
            feedbacks = []
        create_poll_request = CreatePollRequest(
            request.principal,
            request.json.get("community_name"),
            request.json.get("community_size"),
            [
                Feedback(feedback.get("bothers"), feedback.get("age"))
                for feedback in feedbacks
                if isinstance(feedback, dict) is True
            ]
        )
        return self.use_case.create_poll(create_poll_request)

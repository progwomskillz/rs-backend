import csv
from io import StringIO

from ..auth_base_handler import AuthBaseHandler
from domain.entities.polls.requests import CreatePollRequest
from domain.entities.polls import Feedback
from domain.utils import TypesHelper


class CreatePollHandler(AuthBaseHandler):
    def execute(self, request):
        feedbacks = []
        file = request.files.get("file")
        fileio = StringIO(file.read().decode())
        reader = csv.reader(fileio, delimiter=",")
        for i, row in enumerate(reader):
            if i == 0:
                continue
            feedbacks.append({
                "bothers": row[0] if 0 < len(row) else None,
                "age": TypesHelper.try_to_int(row[1]) if 1 < len(row) else None
            })
        create_poll_request = CreatePollRequest(
            request.principal,
            request.form.get("community_name"),
            request.form.get("community_size"),
            [
                Feedback(feedback.get("bothers"), feedback.get("age"))
                for feedback in feedbacks
            ]
        )
        return self.use_case.create_poll(create_poll_request)

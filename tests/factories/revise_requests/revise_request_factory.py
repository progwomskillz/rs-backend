from domain.entities.revise_requests import ReviseRequest
from ..users import UserFactory
from ..polls import PollFactory


class ReviseRequestFactory():
    @staticmethod
    def generic():
        return ReviseRequest(
            "test_id",
            UserFactory.public_official(),
            PollFactory.generic()
        )

    @staticmethod
    def generate(id, user, poll):
        return ReviseRequest(id, user, poll)

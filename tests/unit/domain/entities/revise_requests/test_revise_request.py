from domain.entities.revise_requests import ReviseRequest
from tests.factories.polls import PollFactory
from tests.factories.users import UserFactory


class TestReviseRequest():
    def setup_method(self):
        self.id = "test_id"
        self.user = UserFactory.public_official()
        self.poll = PollFactory.generic()

        self.entity = ReviseRequest(self.id, self.user, self.poll)

    def test_init(self):
        assert self.entity.id == self.id
        assert self.entity.user == self.user
        assert self.entity.poll == self.poll

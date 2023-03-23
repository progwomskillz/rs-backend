from mock import Mock

from domain.entities.polls.requests import CreatePollRequest
from tests.factories.polls import FeedbackFactory


class TestCreatePollRequest():
    def setup_method(self):
        self.principal_mock = Mock()
        self.community_name = "test_community_name"
        self.community_size = "test_community_size"
        self.feedbacks = [
            FeedbackFactory.generic()
            for _ in range(5)
        ]

        self.entity = CreatePollRequest(
            self.principal_mock,
            self.community_name,
            self.community_size,
            self.feedbacks
        )

    def test_init(self):
        assert self.entity.principal == self.principal_mock
        assert self.entity.community_name == self.community_name
        assert self.entity.community_size == self.community_size
        assert self.entity.feedbacks == self.feedbacks

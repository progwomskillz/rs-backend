from datetime import datetime

from domain.entities.polls import Poll
from tests.factories.polls import FeedbackFactory, StatsFactory
from tests.factories.users import UserFactory


class TestPoll():
    def setup_method(self):
        self.id = "test_id"
        self.user = UserFactory.community_social_worker()
        self.updated_at = datetime.utcnow()
        self.community_name = "test_community_name"
        self.community_size = "test_community_size"
        self.feedbacks = [
            FeedbackFactory.generic()
            for _ in range(5)
        ]
        self.summary = [
            StatsFactory.generic()
            for _ in range(3)
        ]

        self.entity = Poll(
            self.id,
            self.user,
            self.updated_at,
            self.community_name,
            self.community_size,
            self.feedbacks,
            self.summary
        )

    def test_init(self):
        assert self.entity.id == self.id
        assert self.entity.user == self.user
        assert self.entity.updated_at == self.updated_at
        assert self.entity.community_name == self.community_name
        assert self.entity.community_size == self.community_size
        assert self.entity.feedbacks == self.feedbacks
        assert self.entity.summary == self.summary

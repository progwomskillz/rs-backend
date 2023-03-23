from datetime import datetime

from domain.entities.polls import Poll
from .feedback_factory import FeedbackFactory
from .stats_factory import StatsFactory
from ..users import UserFactory


class PollFactory():
    @staticmethod
    def generic():
        return Poll(
            "test_id",
            UserFactory.community_social_worker(),
            datetime.utcnow(),
            "test_community_name",
            "test_community_size",
            [
                FeedbackFactory.generic()
                for _ in range(10)
            ],
            [
                StatsFactory.generic()
                for _ in range(3)
            ]
        )

    @staticmethod
    def generate(
        id, user, updated_at, community_name, community_size, feedbacks, summary
    ):
        return Poll(
            id,
            user,
            updated_at,
            community_name,
            community_size,
            feedbacks,
            summary
        )

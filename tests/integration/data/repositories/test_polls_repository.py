from application.structure import structure
from domain.entities.polls import Poll
from tests.factories.polls import FeedbackFactory, PollFactory
from tests.factories.users import UserFactory


class TestPollsRepository():
    def setup_method(self):
        self.repository = structure.polls_repository

        self.users_repository = structure.users_repository

    def teardown_method(self):
        self.repository.collection.delete_many({})
        self.users_repository.collection.delete_many({})

    def test_find_by_id_default_pipeline(self):
        user = UserFactory.community_social_worker()
        user.on_create(self.users_repository.create(user))

        feedbacks = [
            FeedbackFactory.generate("asasdq familysdfnjl", 24),
            FeedbackFactory.generate("asasdq family", 24),
            FeedbackFactory.generate("family asdas", 23),
            FeedbackFactory.generate("family asdas", 26),
            FeedbackFactory.generate("asasdq healthsdfnjl", 24),
            FeedbackFactory.generate("asasdq health", 24),
            FeedbackFactory.generate("health asdas", 23),
            FeedbackFactory.generate("health asdas", 17),
            FeedbackFactory.generate("something", 22),
            FeedbackFactory.generate("something", 56)
        ]
        poll = PollFactory.generate(
            None,
            user,
            None,
            "test_community_name",
            100,
            feedbacks,
            None
        )
        poll_id = self.repository.create(poll)

        result = self.repository.find_by_id(poll_id)

        assert isinstance(result, Poll) is True
        assert result.id == poll_id
        assert result.user.id == user.id
        assert result.updated_at is None
        assert result.community_name == "test_community_name"
        assert result.community_size == 100
        assert len(result.feedbacks) == len(feedbacks)
        for i, feedback in enumerate(result.feedbacks):
            assert feedback.bothers == feedbacks[i].bothers
            assert feedback.age == feedbacks[i].age
        assert len(result.summary) == 3
        assert result.summary[0].title == "family"
        assert result.summary[0].count == 3
        assert result.summary[0].percentage == 30
        assert result.summary[1].title == "health"
        assert result.summary[1].count == 3
        assert result.summary[1].percentage == 30
        assert result.summary[2].title == "unknown"
        assert result.summary[2].count == 4
        assert result.summary[2].percentage == 40

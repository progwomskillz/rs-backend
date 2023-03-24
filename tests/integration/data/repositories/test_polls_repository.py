from bson import ObjectId

from application.structure import structure
from domain.entities.polls import Poll
from domain.entities.shared import Page
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

    def test_get_page_user_id(self):
        user = UserFactory.community_social_worker()
        user.id = str(ObjectId())
        user.on_create(self.users_repository.create(user))

        page = 1
        page_size = 10

        for _ in range(page * page_size + 1):
            poll = PollFactory.generic()
            poll.user = user
            self.repository.create(poll)

        for _ in range(page * page_size + 1):
            temp_user = UserFactory.community_social_worker()
            temp_user.id = str(ObjectId())
            temp_user.on_create(self.users_repository.create(temp_user))
            poll = PollFactory.generic()
            poll.user = temp_user
            self.repository.create(poll)

        result = self.repository.get_page(user.id, page, page_size)

        assert isinstance(result, Page) is True
        assert len(result.items) == page_size
        assert result.page == page
        assert result.page_count == page + 1

    def test_get_page(self):
        user = UserFactory.community_social_worker()
        user.id = str(ObjectId())
        user.on_create(self.users_repository.create(user))

        page = 1
        page_size = 10

        for _ in range(page * page_size + 1):
            poll = PollFactory.generic()
            poll.user = user
            self.repository.create(poll)

        for _ in range(page * page_size + 1):
            temp_user = UserFactory.community_social_worker()
            temp_user.id = str(ObjectId())
            temp_user.on_create(self.users_repository.create(temp_user))
            poll = PollFactory.generic()
            poll.user = temp_user
            self.repository.create(poll)

        result = self.repository.get_page(None, page, page_size)

        assert isinstance(result, Page) is True
        assert len(result.items) == page_size
        assert result.page == page
        assert result.page_count == page * 2 + 1

    def test_get_summary(self):
        for _ in range(2):
            temp_user = UserFactory.community_social_worker()
            temp_user.id = str(ObjectId())
            temp_user.on_create(self.users_repository.create(temp_user))
            poll = PollFactory.generic()
            poll.user = temp_user
            self.repository.create(poll)

        result = self.repository.get_summary()

        assert isinstance(result, list) is True
        assert len(result) == 3
        assert result[0].title == "family"
        assert result[0].count == 20
        assert result[0].percentage == 100
        assert result[1].title == "health"
        assert result[1].count == 20
        assert result[1].percentage == 100
        assert result[2].title == "unknown"
        assert result[2].count == 0
        assert result[2].percentage == 0

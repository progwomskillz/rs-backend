from bson import ObjectId

from application.structure import structure
from domain.entities.polls import Poll
from domain.entities.revise_requests import ReviseRequest
from domain.entities.shared import Page
from domain.entities.users import User
from tests.factories.polls import FeedbackFactory, PollFactory
from tests.factories.revise_requests import ReviseRequestFactory
from tests.factories.users import UserFactory


class TestMongoReviseRequestsRepository():
    def setup_method(self):
        self.repository = structure.mongo_revise_requests_repository

        self.users_repository = structure.mongo_users_repository
        self.polls_repository = structure.mongo_polls_repository

    def teardown_method(self):
        self.repository.collection.delete_many({})
        self.users_repository.collection.delete_many({})
        self.polls_repository.collection.delete_many({})

    def test_find_by_id_default_pipeline(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        poll = PollFactory.generic()
        poll.user.on_create(self.users_repository.create(poll.user))
        poll.id = self.polls_repository.create(poll)

        revise_request = ReviseRequestFactory.generate(None, user, poll)
        revise_request_id = self.repository.create(revise_request)

        result = self.repository.find_by_id(revise_request_id)

        assert isinstance(result, ReviseRequest) is True
        assert result.id == revise_request_id
        assert isinstance(result.user, User) is True
        assert result.user.id == user.id
        assert isinstance(result.poll, Poll) is True
        assert result.poll.id == poll.id
        assert isinstance(result.poll.user, User) is True
        assert result.poll.user.id == poll.user.id

    def test_get_page(self):
        user = UserFactory.community_social_worker()
        user.on_create(self.users_repository.create(user))
        poll = PollFactory.generate(
            None,
            user,
            None,
            "test_community_name",
            25,
            [FeedbackFactory.generic()],
            None
        )
        poll.id = self.polls_repository.create(poll)

        page = 1
        page_size = 10

        for _ in range(page * page_size + 1):
            revise_request = ReviseRequestFactory.generic()
            revise_request.user.on_create(self.users_repository.create(revise_request.user))
            revise_request.poll = poll
            self.repository.create(revise_request)

        for _ in range(page * page_size + 1):
            revise_request = ReviseRequestFactory.generic()
            revise_request.user.on_create(self.users_repository.create(revise_request.user))
            revise_request.poll = PollFactory.generic()
            revise_request.poll.user.on_create(self.users_repository.create(
                revise_request.poll.user
            ))
            revise_request.poll.id = self.polls_repository.create(revise_request.poll)
            self.repository.create(revise_request)

        result = self.repository.get_page(user.id, page, page_size)

        assert isinstance(result, Page) is True
        assert len(result.items) == page_size
        assert result.page == page
        assert result.page_count == page + 1

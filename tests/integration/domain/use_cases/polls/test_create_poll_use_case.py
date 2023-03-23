import pytest

from application.structure import structure
from data.repositories import PollsRepository
from domain.entities.auth import TokensPayload, Principal
from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException,
    InvalidRequest
)
from domain.entities.polls.requests import CreatePollRequest
from domain.entities.polls import Poll
from domain.utils.validation import PrincipalValidationUtil, RBACValidationUtil
from domain.utils.validation.polls import CreatePollRequestValidationUtil
from tests.factories.polls import FeedbackFactory
from tests.factories.users import UserFactory


class TestCreatePollUseCase():
    def setup_method(self):
        self.use_case = structure.create_poll_use_case

        self.polls_repository = structure.polls_repository
        self.users_repository = structure.users_repository

    def teardown_method(self):
        self.polls_repository.collection.delete_many({})
        self.users_repository.collection.delete_many({})

    def test_init(self):
        assert isinstance(
            self.use_case.principal_validation_util,
            PrincipalValidationUtil
        ) is True
        assert isinstance(
            self.use_case.rbac_validation_util,
            RBACValidationUtil
        ) is True
        assert isinstance(
            self.use_case.create_poll_request_validation_util,
            CreatePollRequestValidationUtil
        ) is True
        assert isinstance(
            self.use_case.polls_repository,
            PollsRepository
        ) is True

    def test_create_poll_invalid_principal(self):
        principal = None
        community_name = None
        community_size = None
        feedbacks = None
        create_poll_request = CreatePollRequest(
            principal,
            community_name,
            community_size,
            feedbacks
        )

        with pytest.raises(UnauthenticatedException):
            self.use_case.create_poll(create_poll_request)

    def test_create_poll_invalid_principal_role(self):
        user = UserFactory.admin()
        principal = Principal(user, None)
        community_name = None
        community_size = None
        feedbacks = None
        create_poll_request = CreatePollRequest(
            principal,
            community_name,
            community_size,
            feedbacks
        )

        with pytest.raises(UnauthorizedException):
            self.use_case.create_poll(create_poll_request)

    def test_create_poll_invalid_request(self):
        user = UserFactory.community_social_worker()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        community_name = None
        community_size = None
        feedbacks = None
        create_poll_request = CreatePollRequest(
            principal,
            community_name,
            community_size,
            feedbacks
        )

        with pytest.raises(InvalidRequest) as e:
            self.use_case.create_poll(create_poll_request)

        assert e.value.errors == {
            "community_name": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ],
            "community_size": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ],
            "feedbacks": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"array\"",
                    "code": "type"
                }
            ]
        }

    def test_create_poll(self):
        user = UserFactory.community_social_worker()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        community_name = "test_community_name"
        community_size = 25
        feedbacks = [FeedbackFactory.generic()]
        create_poll_request = CreatePollRequest(
            principal,
            community_name,
            community_size,
            feedbacks
        )

        result = self.use_case.create_poll(create_poll_request)

        assert isinstance(result, Poll) is True
        assert result.user.email == user.email
        assert result.updated_at is None
        assert result.community_name == community_name
        assert result.community_size == community_size
        assert len(result.feedbacks) == 1
        assert result.feedbacks[0].bothers == feedbacks[0].bothers
        assert result.feedbacks[0].age == feedbacks[0].age
        assert len(result.summary) == 3
        assert result.summary[0].title == "family"
        assert result.summary[0].count == 1
        assert result.summary[0].percentage == 100
        assert result.summary[1].title == "health"
        assert result.summary[1].count == 1
        assert result.summary[1].percentage == 100
        assert result.summary[2].title == "unknown"
        assert result.summary[2].count == 0
        assert result.summary[2].percentage == 0

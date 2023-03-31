import pytest

from application.structure import structure
from data.repositories.mongo import MongoReviseRequestsRepository
from domain.entities.auth import TokensPayload, Principal
from domain.entities.exceptions import (
    InvalidRequest,
    NotFoundException,
    UnauthenticatedException,
    UnauthorizedException
)
from domain.entities.polls import Poll
from domain.entities.revise_requests.requests import CreateReviseRequestRequest
from domain.entities.revise_requests import ReviseRequest
from domain.entities.users import User
from domain.utils.validation import PrincipalValidationUtil, RBACValidationUtil
from domain.utils.validation.revise_requests import (
    CreateReviseRequestRequestValidationUtil
)
from tests.factories.polls import PollFactory
from tests.factories.users import UserFactory


class TestCreateReviseRequestUseCase():
    def setup_method(self):
        self.use_case = structure.create_revise_request_use_case

        self.revise_requests_repository = structure.mongo_revise_requests_repository
        self.users_repository = structure.mongo_users_repository
        self.polls_repository = structure.mongo_polls_repository

    def teardown_method(self):
        self.revise_requests_repository.collection.delete_many({})
        self.users_repository.collection.delete_many({})
        self.polls_repository.collection.delete_many({})

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
            self.use_case.create_revise_request_request_validation_util,
            CreateReviseRequestRequestValidationUtil
        ) is True
        assert isinstance(
            self.use_case.revise_requests_repository,
            MongoReviseRequestsRepository
        ) is True

    def test_create_revise_request_invalid_principal(self):
        principal = None
        create_revise_request_request = CreateReviseRequestRequest(
            principal,
            None
        )

        with pytest.raises(UnauthenticatedException):
            self.use_case.create_revise_request(create_revise_request_request)

    def test_create_revise_request_invalid_principal_role(self):
        user = UserFactory.community_social_worker()
        principal = Principal(user, None)
        poll_id = None
        create_revise_request_request = CreateReviseRequestRequest(
            principal,
            poll_id
        )

        with pytest.raises(UnauthorizedException):
            self.use_case.create_revise_request(create_revise_request_request)

    def test_create_revise_request_invalid_request(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        poll_id = None
        create_revise_request_request = CreateReviseRequestRequest(
            principal,
            poll_id
        )

        with pytest.raises(InvalidRequest) as e:
            self.use_case.create_revise_request(create_revise_request_request)

        assert e.value.errors == {
            "poll_id": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ]
        }

    def test_create_revise_request_poll_not_found(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        poll = PollFactory.generic()
        create_revise_request_request = CreateReviseRequestRequest(
            principal,
            poll.id
        )

        with pytest.raises(NotFoundException):
            self.use_case.create_revise_request(create_revise_request_request)

    def test_create_revise_request(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        poll = PollFactory.generic()
        poll.user.on_create(self.users_repository.create(poll.user))
        poll.id = self.polls_repository.create(poll)

        principal = Principal(user, tokens_pair)
        create_revise_request_request = CreateReviseRequestRequest(
            principal,
            poll.id
        )

        result = self.use_case.create_revise_request(create_revise_request_request)

        assert isinstance(result, ReviseRequest) is True
        assert isinstance(result.user, User) is True
        assert result.user.id == user.id
        assert isinstance(result.poll, Poll) is True
        assert result.poll.id == poll.id

        result_revise_request = self.revise_requests_repository.find_by_id(
            result.id
        )
        assert isinstance(result_revise_request, ReviseRequest) is True

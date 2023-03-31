import pytest

from application.structure import structure
from data.repositories.mongo import MongoPollsRepository
from domain.entities.auth import Principal, TokensPayload
from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException,
    InvalidRequest
)
from domain.entities.shared import Page
from domain.entities.polls.requests import GetPollsPageRequest
from domain.entities.polls import Poll
from domain.utils.validation.polls import GetPollsPageRequestValidationUtil
from domain.utils.validation import PrincipalValidationUtil, RBACValidationUtil
from tests.factories.polls import PollFactory
from tests.factories.users import UserFactory


class TestGetPollsPageUseCase():
    def setup_method(self):
        self.use_case = structure.get_polls_page_use_case

        self.polls_repository = structure.mongo_polls_repository
        self.users_repository = structure.mongo_users_repository

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
            self.use_case.get_polls_page_request_validation_util,
            GetPollsPageRequestValidationUtil
        ) is True
        assert isinstance(
            self.use_case.polls_repository,
            MongoPollsRepository
        ) is True

    def test_get_polls_page_invalid_principal(self):
        principal = None
        page = None
        page_size = None
        get_polls_page_request = GetPollsPageRequest(
            principal,
            page,
            page_size
        )

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_polls_page(get_polls_page_request)

    def test_get_polls_page_invalid_principal_role(self):
        user = UserFactory.admin()
        principal = Principal(user, None)
        page = None
        page_size = None
        get_polls_page_request = GetPollsPageRequest(
            principal,
            page,
            page_size
        )

        with pytest.raises(UnauthorizedException):
            self.use_case.get_polls_page(get_polls_page_request)

    def test_get_polls_page_invalid_request_user_id(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        page = None
        page_size = None
        get_polls_page_request = GetPollsPageRequest(
            principal,
            page,
            page_size
        )

        with pytest.raises(InvalidRequest) as e:
            self.use_case.get_polls_page(get_polls_page_request)

        assert e.value.errors == {
            "page": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ],
            "page_size": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ]
        }

    def test_get_polls_page_invalid_request(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        page = None
        page_size = None
        get_polls_page_request = GetPollsPageRequest(
            principal,
            page,
            page_size
        )

        with pytest.raises(InvalidRequest) as e:
            self.use_case.get_polls_page(get_polls_page_request)

        assert e.value.errors == {
            "page": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ],
            "page_size": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ]
        }

    def test_get_polls_page(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)

        page = 1
        page_size = 10
        get_polls_page_request = GetPollsPageRequest(
            principal,
            page,
            page_size
        )

        for _ in range(page * page_size + 1):
            temp_user = UserFactory.community_social_worker()
            temp_user.on_create(self.users_repository.create(temp_user))
            poll = PollFactory.generic()
            poll.user = temp_user
            self.polls_repository.create(poll)

        result = self.use_case.get_polls_page(get_polls_page_request)

        assert isinstance(result, Page) is True
        assert len(result.items) == page_size
        assert result.page == page
        assert result.page_count == page + 1
        for item in result.items:
            assert isinstance(item, Poll) is True

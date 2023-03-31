import pytest

from application.structure import structure
from data.repositories.mongo import MongoReviseRequestsRepository
from domain.entities.auth import Principal, TokensPayload
from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException,
    InvalidRequest
)
from domain.entities.shared import Page
from domain.entities.revise_requests.requests import GetReviseRequestsPageRequest
from domain.entities.revise_requests import ReviseRequest
from domain.utils.validation.revise_requests import GetReviseRequestsPageRequestValidationUtil
from domain.utils.validation import PrincipalValidationUtil, RBACValidationUtil
from tests.factories.polls import FeedbackFactory, PollFactory
from tests.factories.revise_requests import ReviseRequestFactory
from tests.factories.users import UserFactory


class TestGetReviseRequestsPageUseCase():
    def setup_method(self):
        self.use_case = structure.get_revise_requests_page_use_case

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
            self.use_case.get_revise_requests_page_request_validation_util,
            GetReviseRequestsPageRequestValidationUtil
        ) is True
        assert isinstance(
            self.use_case.revise_requests_repository,
            MongoReviseRequestsRepository
        ) is True

    def test_get_revise_requests_page_invalid_principal(self):
        principal = None
        page = None
        page_size = None
        get_revise_requests_page_request = GetReviseRequestsPageRequest(
            principal,
            page,
            page_size
        )

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_revise_requests_page(
                get_revise_requests_page_request
            )

    def test_get_revise_requests_page_invalid_principal_role(self):
        user = UserFactory.admin()
        principal = Principal(user, None)
        page = None
        page_size = None
        get_revise_requests_page_request = GetReviseRequestsPageRequest(
            principal,
            page,
            page_size
        )

        with pytest.raises(UnauthorizedException):
            self.use_case.get_revise_requests_page(get_revise_requests_page_request)

    def test_get_revise_requests_page_invalid_request(self):
        user = UserFactory.community_social_worker()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        page = None
        page_size = None
        get_revise_requests_page_request = GetReviseRequestsPageRequest(
            principal,
            page,
            page_size
        )

        with pytest.raises(InvalidRequest) as e:
            self.use_case.get_revise_requests_page(get_revise_requests_page_request)

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

    def test_get_revise_requests_page(self):
        user = UserFactory.community_social_worker()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)
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

        principal = Principal(user, tokens_pair)

        page = 1
        page_size = 10
        get_revise_requests_page_request = GetReviseRequestsPageRequest(
            principal,
            page,
            page_size
        )

        for _ in range(page * page_size + 1):
            revise_request = ReviseRequestFactory.generic()
            revise_request.user.on_create(self.users_repository.create(revise_request.user))
            revise_request.poll = poll
            self.revise_requests_repository.create(revise_request)

        result = self.use_case.get_revise_requests_page(
            get_revise_requests_page_request
        )

        assert isinstance(result, Page) is True
        assert len(result.items) == page_size
        assert result.page == page
        assert result.page_count == page + 1
        for item in result.items:
            assert isinstance(item, ReviseRequest) is True

import pytest

from application.structure import structure
from data.repositories import PollsRepository
from domain.entities.auth import Principal, TokensPayload
from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException
)
from domain.entities.shared import Page
from domain.entities.polls.requests import GetPollsSummaryRequest
from domain.entities.polls import Poll
from domain.utils.validation import PrincipalValidationUtil, RBACValidationUtil
from tests.factories.polls import PollFactory
from tests.factories.users import UserFactory


class TestGetPollsSummaryUseCase():
    def setup_method(self):
        self.use_case = structure.get_polls_summary_use_case

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
            self.use_case.polls_repository,
            PollsRepository
        ) is True

    def test_get_polls_summary_invalid_principal(self):
        principal = None
        get_polls_summary_request = GetPollsSummaryRequest(principal)

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_polls_summary(get_polls_summary_request)

    def test_get_polls_summary_invalid_principal_role(self):
        user = UserFactory.admin()
        principal = Principal(user, None)
        get_polls_summary_request = GetPollsSummaryRequest(principal)

        with pytest.raises(UnauthorizedException):
            self.use_case.get_polls_summary(get_polls_summary_request)

    def test_get_polls_summary(self):
        user = UserFactory.public_official()
        user.on_create(self.users_repository.create(user))
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)

        user_id = None
        get_polls_summary_request = GetPollsSummaryRequest(principal)

        for _ in range(2):
            temp_user = UserFactory.community_social_worker()
            temp_user.on_create(self.users_repository.create(temp_user))
            poll = PollFactory.generic()
            poll.user = temp_user
            self.polls_repository.create(poll)

        result = self.use_case.get_polls_summary(get_polls_summary_request)

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

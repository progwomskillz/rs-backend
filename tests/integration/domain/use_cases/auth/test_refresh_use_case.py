import pytest

from application.structure import structure
from data.repositories import UsersRepository
from data.utils.wrappers import JWTWrapper
from domain.entities.auth.requests import RefreshRequest
from domain.entities.auth import TokensPair, TokensPayload
from domain.entities.exceptions import InvalidRequest, UnauthenticatedException
from domain.utils.validation.auth import RefreshRequestValidationUtil
from tests.factories.users import UserFactory


class TestRefreshUseCase():
    def setup_method(self):
        self.use_case = structure.refresh_use_case

        self.users_repository = structure.users_repository

    def teardown_method(self):
        self.users_repository.collection.delete_many({})

    def test_init(self):
        assert isinstance(
            self.use_case.refresh_request_validation_util,
            RefreshRequestValidationUtil
        ) is True
        assert isinstance(
            self.use_case.users_repository,
            UsersRepository
        ) is True
        assert isinstance(
            self.use_case.tokens_util,
            JWTWrapper
        ) is True

    def test_refresh_invalid(self):
        refresh_request = RefreshRequest(None)

        with pytest.raises(InvalidRequest) as e:
            self.use_case.refresh(refresh_request)

        assert e.value.errors == {
            "refresh": [
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

    def test_refresh_token_invalid(self):
        refresh_request = RefreshRequest("test_refresh")

        with pytest.raises(UnauthenticatedException):
            self.use_case.refresh(refresh_request)

    def test_refresh_user_not_found(self):
        tokens_payload = TokensPayload("test_user_id", "test_user_role")
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        refresh_request = RefreshRequest(tokens_pair.refresh)

        with pytest.raises(UnauthenticatedException):
            self.use_case.refresh(refresh_request)

    def test_refresh_token_doesnt_exist(self):
        user = UserFactory.admin()

        user_id = self.users_repository.create(user)
        user.on_create(user_id)

        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        refresh_request = RefreshRequest(tokens_pair.refresh)

        with pytest.raises(UnauthenticatedException):
            self.use_case.refresh(refresh_request)

    def test_refresh(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        refresh_request = RefreshRequest(tokens_pair.refresh)

        result = self.use_case.refresh(refresh_request)

        assert isinstance(result, TokensPair) is True
        assert isinstance(result.access, str) is True
        assert len(result.access) > 0
        assert result.access != tokens_pair.access
        assert isinstance(result.refresh, str) is True
        assert len(result.refresh) > 0
        assert result.refresh == tokens_pair.refresh

        result_user = self.users_repository.find_by_id(user.id)
        assert len(result_user.tokens_pairs) == 1
        tokens_pair = result_user.tokens_pairs[0]
        assert tokens_pair.access == result.access
        assert tokens_pair.refresh == result.refresh

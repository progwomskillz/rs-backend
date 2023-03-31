import pytest

from application.structure import structure
from data.repositories.mongo import MongoUsersRepository
from data.utils.wrappers import BcryptWrapper, JWTWrapper
from domain.entities.auth.requests import LoginRequest
from domain.entities.auth import TokensPair
from domain.entities.exceptions import InvalidRequest, UnauthenticatedException
from domain.utils.validation.auth import LoginRequestValidationUtil
from tests.factories.users import UserFactory


class TestLoginUseCase():
    def setup_method(self):
        self.use_case = structure.login_use_case

        self.users_repository = structure.mongo_users_repository

    def teardown_method(self):
        self.users_repository.collection.delete_many({})

    def test_init(self):
        assert isinstance(
            self.use_case.login_request_validation_util,
            LoginRequestValidationUtil
        ) is True
        assert isinstance(
            self.use_case.users_repository,
            MongoUsersRepository
        ) is True
        assert isinstance(
            self.use_case.password_util,
            BcryptWrapper
        ) is True
        assert isinstance(
            self.use_case.tokens_util,
            JWTWrapper
        ) is True

    def test_login_invalid(self):
        login_request = LoginRequest(None, None)

        with pytest.raises(InvalidRequest) as e:
            self.use_case.login(login_request)

        assert e.value.errors == {
            "username": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ],
            "password": [
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

    def test_login_user_not_found(self):
        login_request = LoginRequest("test@example.com", "test_password")

        with pytest.raises(UnauthenticatedException):
            self.use_case.login(login_request)

    def test_login_wrong_password(self):
        user = UserFactory.admin()
        self.users_repository.create(user)

        login_request = LoginRequest(user.username, "test_wrong_password")

        with pytest.raises(UnauthenticatedException):
            self.use_case.login(login_request)

    def test_login(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)

        login_request = LoginRequest(user.username, UserFactory.get_password())

        result = self.use_case.login(login_request)

        assert isinstance(result, TokensPair) is True
        assert isinstance(result.access, str) is True
        assert len(result.access) > 0
        assert isinstance(result.refresh, str) is True
        assert len(result.refresh) > 0

        result_user = self.users_repository.find_by_id(user.id)
        assert len(result_user.tokens_pairs) == 1
        tokens_pair = result_user.tokens_pairs[0]
        assert tokens_pair.access == result.access
        assert tokens_pair.refresh == result.refresh

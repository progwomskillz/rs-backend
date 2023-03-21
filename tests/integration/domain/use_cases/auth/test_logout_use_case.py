import pytest

from application.structure import structure
from data.repositories import UsersRepository
from domain.entities.auth.requests import LogoutRequest
from domain.entities.auth import TokensPayload, Principal
from domain.entities.exceptions import UnauthenticatedException
from domain.utils.validation import PrincipalValidationUtil
from tests.factories.users import UserFactory


class TestLogoutUseCase():
    def setup_method(self):
        self.use_case = structure.logout_use_case

        self.users_repository = structure.users_repository

    def teardown_method(self):
        self.users_repository.collection.delete_many({})

    def test_init(self):
        assert isinstance(
            self.use_case.principal_validation_util,
            PrincipalValidationUtil
        ) is True
        assert isinstance(
            self.use_case.users_repository,
            UsersRepository
        ) is True

    def test_logout_invalid_principal(self):
        principal = None
        logout_request = LogoutRequest(principal)

        with pytest.raises(UnauthenticatedException):
            self.use_case.logout(logout_request)

    def test_logout(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        logout_request = LogoutRequest(principal)

        self.use_case.logout(logout_request)

        result_user = self.users_repository.find_by_id(user.id)
        assert len(result_user.tokens_pairs) == 0

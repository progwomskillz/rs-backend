import os

from application.structure import structure
from data.repositories import UsersRepository
from data.utils.wrappers import JWTWrapper
from domain.entities.auth import TokensPayload, Principal, TokensPair
from domain.entities.users import User
from tests.factories.users import UserFactory


class TestPrincipalUtil():
    def setup_method(self):
        self.util = structure.principal_util

        self.users_repository = structure.users_repository

    def teardown_method(self):
        self.users_repository.collection.delete_many({})

    def test_init(self):
        assert self.util.allowed_token_type == os.environ["JWT_TYPE"].lower()
        assert isinstance(self.util.tokens_util, JWTWrapper) is True
        assert isinstance(self.util.users_repository, UsersRepository) is True

    def test_get_authorization_header_not_str(self):
        authorization_header = 123

        result = self.util.get(authorization_header)

        assert result is None

    def test_get_authorization_header_len_not_2(self):
        authorization_header = "test_authorization_header"

        result = self.util.get(authorization_header)

        assert result is None

    def test_get_invalid_token_type(self):
        token = "test_token"
        authorization_header = f"{self.util.allowed_token_type}_wrong {token}"

        result = self.util.get(authorization_header)

        assert result is None

    def test_get_invalid_not_tokens_payload(self):
        token = "test_token"
        authorization_header = f"{self.util.allowed_token_type} {token}"

        result = self.util.get(authorization_header)

        assert result is None

    def test_get_user_not_found(self):
        user_id = "test_user_id"
        user_role = "test_user_role"
        tokens_payload = TokensPayload(user_id, user_role)
        tokens_pair = self.util.tokens_util.create_pair(tokens_payload)
        token = tokens_pair.access
        authorization_header = f"{self.util.allowed_token_type} {token}"

        result = self.util.get(authorization_header)

        assert result is None

    def test_get_tokens_pair_not_found(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = self.util.tokens_util.create_pair(tokens_payload)
        token = tokens_pair.access
        authorization_header = f"{self.util.allowed_token_type} {token}"

        result = self.util.get(authorization_header)

        assert result is None

    def test_get(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = self.util.tokens_util.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)
        token = tokens_pair.access
        authorization_header = f"{self.util.allowed_token_type} {token}"

        result = self.util.get(authorization_header)

        assert isinstance(result, Principal) is True
        assert isinstance(result.user, User) is True
        assert result.user.id == user.id
        assert isinstance(result.tokens_pair, TokensPair) is True
        assert result.tokens_pair.access == tokens_pair.access
        assert result.tokens_pair.refresh == tokens_pair.refresh

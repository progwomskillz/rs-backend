import pytest
from mock import Mock, patch

from domain.use_cases.auth import LoginUseCase
from domain.entities.exceptions import InvalidRequest, UnauthenticatedException


class TestLoginUseCase():
    def setup_method(self):
        self.login_request_validation_util_mock = Mock()
        self.users_repository_mock = Mock()
        self.password_util_mock = Mock()
        self.tokens_util_mock = Mock()

        self.use_case = LoginUseCase(
            self.login_request_validation_util_mock,
            self.users_repository_mock,
            self.password_util_mock,
            self.tokens_util_mock
        )

    def test_init(self):
        assert self.use_case.login_request_validation_util ==\
            self.login_request_validation_util_mock
        assert self.use_case.users_repository == self.users_repository_mock
        assert self.use_case.password_util == self.password_util_mock
        assert self.use_case.tokens_util == self.tokens_util_mock

    def test_login_invalid_request(self):
        login_request_mock = Mock()
        login_request_mock.username = None
        login_request_mock.password = None

        validation_errors = {}
        self.login_request_validation_util_mock.validate.side_effect = [
            InvalidRequest(validation_errors)
        ]

        with pytest.raises(InvalidRequest) as e:
            self.use_case.login(login_request_mock)

        assert e.value.errors == validation_errors

        self.login_request_validation_util_mock.validate.assert_called_once_with(
            login_request_mock
        )
        self.users_repository_mock.find_by_username.assert_not_called()
        self.password_util_mock.compare.assert_not_called()
        self.tokens_util_mock.create_pair.assert_not_called()
        self.users_repository_mock.update.assert_not_called()

    def test_login_user_not_found(self):
        login_request_mock = Mock()
        login_request_mock.username = "test_username"
        login_request_mock.password = "test_password"

        self.users_repository_mock.find_by_username.return_value = None

        with pytest.raises(UnauthenticatedException):
            self.use_case.login(login_request_mock)

        self.login_request_validation_util_mock.validate.assert_called_once_with(
            login_request_mock
        )
        self.users_repository_mock.find_by_username.assert_called_once_with(
            login_request_mock.username
        )
        self.password_util_mock.compare.assert_not_called()
        self.tokens_util_mock.create_pair.assert_not_called()
        self.users_repository_mock.update.assert_not_called()

    def test_login_user_wrong_password(self):
        login_request_mock = Mock()
        login_request_mock.username = "test_username"
        login_request_mock.password = "test_password"

        user_mock = Mock()
        user_mock.password_hash = b"test_password_hash"
        self.users_repository_mock.find_by_username.return_value = user_mock
        self.password_util_mock.compare.return_value = False

        with pytest.raises(UnauthenticatedException):
            self.use_case.login(login_request_mock)

        self.login_request_validation_util_mock.validate.assert_called_once_with(
            login_request_mock
        )
        self.users_repository_mock.find_by_username.assert_called_once_with(
            login_request_mock.username
        )
        self.password_util_mock.compare.assert_called_once_with(
            login_request_mock.password,
            user_mock.password_hash
        )
        self.tokens_util_mock.create_pair.assert_not_called()
        self.users_repository_mock.update.assert_not_called()

    @patch("domain.use_cases.auth.login_use_case.TokensPayload")
    def test_login(self, TokensPayload_mock):
        login_request_mock = Mock()
        login_request_mock.username = "test_username"
        login_request_mock.password = "test_password"

        user_mock = Mock()
        user_mock.password_hash = b"test_password_hash"
        user_mock.id = "test_id"
        user_mock.role = "test_role"
        self.users_repository_mock.find_by_username.return_value = user_mock
        self.password_util_mock.compare.return_value = True
        tokens_payload_mock = Mock()
        TokensPayload_mock.return_value = tokens_payload_mock
        tokens_pair_mock = Mock()
        self.tokens_util_mock.create_pair.return_value = tokens_pair_mock

        result = self.use_case.login(login_request_mock)

        assert result == tokens_pair_mock
        self.login_request_validation_util_mock.validate.assert_called_once_with(
            login_request_mock
        )
        self.users_repository_mock.find_by_username.assert_called_once_with(
            login_request_mock.username
        )
        self.password_util_mock.compare.assert_called_once_with(
            login_request_mock.password,
            user_mock.password_hash
        )
        TokensPayload_mock.assert_called_once_with(user_mock.id, user_mock.role)
        self.tokens_util_mock.create_pair.assert_called_once_with(
            tokens_payload_mock
        )
        self.users_repository_mock.update.assert_called_once_with(user_mock)

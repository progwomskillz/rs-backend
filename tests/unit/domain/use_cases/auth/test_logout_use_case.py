import pytest
from mock import Mock

from domain.use_cases.auth import LogoutUseCase
from domain.entities.exceptions import UnauthenticatedException


class TestLogoutUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.users_repository_mock = Mock()

        self.use_case = LogoutUseCase(
            self.principal_validation_util_mock,
            self.users_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.users_repository == self.users_repository_mock

    def test_logout_invalid_principal(self):
        logout_request_mock = Mock()
        logout_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.logout(logout_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            logout_request_mock.principal
        )
        self.users_repository_mock.update.assert_not_called()

    def test_logout(self):
        logout_request_mock = Mock()
        principal_mock = Mock()
        user_mock = Mock()
        principal_mock.user = user_mock
        tokens_pair_mock = Mock()
        principal_mock.tokens_pair = tokens_pair_mock
        logout_request_mock.principal = principal_mock

        self.use_case.logout(logout_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            logout_request_mock.principal
        )
        user_mock.on_logout.assert_called_once_with(tokens_pair_mock)
        self.users_repository_mock.update.assert_called_once_with(user_mock)

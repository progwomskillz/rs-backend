from mock import Mock
import pytest

from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException,
    InvalidRequest
)
from domain.use_cases.users import GetUsersPageUseCase
from domain.utils import constants


class TestGetUsersPageUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.rbac_validation_util_mock = Mock()
        self.get_users_page_request_validation_util_mock = Mock()
        self.users_repository_mock = Mock()

        self.use_case = GetUsersPageUseCase(
            self.principal_validation_util_mock,
            self.rbac_validation_util_mock,
            self.get_users_page_request_validation_util_mock,
            self.users_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.rbac_validation_util ==\
            self.rbac_validation_util_mock
        assert self.use_case.get_users_page_request_validation_util ==\
            self.get_users_page_request_validation_util_mock
        assert self.use_case.users_repository == self.users_repository_mock

    def test_get_users_page_invalid_principal(self):
        get_users_page_request_mock = Mock()
        get_users_page_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_users_page(get_users_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_users_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_not_called()
        self.get_users_page_request_validation_util_mock.validate\
            .assert_not_called()
        self.users_repository_mock.get_page_by_role.assert_not_called()

    def test_get_users_page_invalid_principal_role(self):
        get_users_page_request_mock = Mock()
        principal_mock = Mock()
        get_users_page_request_mock.principal = principal_mock

        self.rbac_validation_util_mock.validate.side_effect = [
            UnauthorizedException()
        ]

        with pytest.raises(UnauthorizedException):
            self.use_case.get_users_page(get_users_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_users_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_users_page_request_mock.principal.user,
            [
                constants.user_roles.admin,
                constants.user_roles.public_official
            ]
        )
        self.get_users_page_request_validation_util_mock.validate\
            .assert_not_called()
        self.users_repository_mock.get_page_by_role.assert_not_called()

    def test_get_users_page_invalid_request(self):
        get_users_page_request_mock = Mock()
        principal_mock = Mock()
        get_users_page_request_mock.principal = principal_mock

        self.get_users_page_request_validation_util_mock.validate.side_effect = [
            InvalidRequest({})
        ]

        with pytest.raises(InvalidRequest):
            self.use_case.get_users_page(get_users_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_users_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_users_page_request_mock.principal.user,
            [
                constants.user_roles.admin,
                constants.user_roles.public_official
            ]
        )
        self.get_users_page_request_validation_util_mock.validate\
            .assert_called_once_with(get_users_page_request_mock)
        self.users_repository_mock.get_page_by_role.assert_not_called()

    def test_get_users_page(self):
        get_users_page_request_mock = Mock()
        principal_mock = Mock()
        get_users_page_request_mock.principal = principal_mock
        get_users_page_request_mock.role = "test_role"
        get_users_page_request_mock.page = 1
        get_users_page_request_mock.page_size = 10

        users_page_mock = Mock()
        self.users_repository_mock.get_page_by_role.return_value = users_page_mock

        result = self.use_case.get_users_page(get_users_page_request_mock)

        assert result == users_page_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_users_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_users_page_request_mock.principal.user,
            [
                constants.user_roles.admin,
                constants.user_roles.public_official
            ]
        )
        self.get_users_page_request_validation_util_mock.validate\
            .assert_called_once_with(get_users_page_request_mock)
        self.users_repository_mock.get_page_by_role.assert_called_once_with(
            get_users_page_request_mock.role,
            get_users_page_request_mock.page,
            get_users_page_request_mock.page_size
        )

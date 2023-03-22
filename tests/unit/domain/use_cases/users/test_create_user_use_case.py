import pytest
from mock import Mock, patch

from domain.entities.exceptions import (
    InvalidRequest,
    UnauthenticatedException,
    UnauthorizedException
)
from domain.use_cases.users import CreateUserUseCase
from domain.utils import constants


class TestCreateUserUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.rbac_validation_util_mock = Mock()
        self.create_user_request_validation_util_mock = Mock()
        self.password_util_mock = Mock()
        self.users_repository_mock = Mock()

        self.use_case = CreateUserUseCase(
            self.principal_validation_util_mock,
            self.rbac_validation_util_mock,
            self.create_user_request_validation_util_mock,
            self.password_util_mock,
            self.users_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.rbac_validation_util ==\
            self.rbac_validation_util_mock
        assert self.use_case.create_user_request_validation_util ==\
            self.create_user_request_validation_util_mock
        assert self.use_case.password_util == self.password_util_mock
        assert self.use_case.users_repository ==\
            self.users_repository_mock

    def test_create_user_invalid_principal(self):
        create_user_request_mock = Mock()
        create_user_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.create_user(create_user_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_not_called()
        self.create_user_request_validation_util_mock.validate.assert_not_called()
        self.password_util_mock.hash.assert_not_called()
        self.users_repository_mock.create.assert_not_called()

    def test_create_user_invalid_principal_role(self):
        create_user_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        create_user_request_mock.principal = principal_mock

        self.rbac_validation_util_mock.validate.side_effect = [
            UnauthorizedException()
        ]

        with pytest.raises(UnauthorizedException):
            self.use_case.create_user(create_user_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock.principal.user,
            [constants.user_roles.admin]
        )
        self.create_user_request_validation_util_mock.validate.assert_not_called()
        self.password_util_mock.hash.assert_not_called()
        self.users_repository_mock.create.assert_not_called()

    def test_create_user_invalid_request(self):
        create_user_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        create_user_request_mock.principal = principal_mock

        self.create_user_request_validation_util_mock.validate.side_effect = [
            InvalidRequest({})
        ]

        with pytest.raises(InvalidRequest):
            self.use_case.create_user(create_user_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock.principal.user,
            [constants.user_roles.admin]
        )
        self.create_user_request_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock
        )
        self.password_util_mock.hash.assert_not_called()
        self.users_repository_mock.create.assert_not_called()

    @patch("domain.use_cases.users.create_user_use_case.User")
    @patch("domain.use_cases.users.create_user_use_case.CommunitySocialWorkerProfile")
    def test_create_user(self, CommunitySocialWorkerProfile_mock, User_mock):
        create_user_request_mock = Mock()
        create_user_request_mock.role = constants.user_roles\
            .community_social_worker
        create_user_request_mock.email = "test@example.com"
        create_user_request_mock.password = "test_password"
        create_user_request_mock.first_name = "test_first_name"
        create_user_request_mock.last_name = "test_last_name"
        principal_user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = principal_user_mock
        create_user_request_mock.principal = principal_mock

        user_mock = Mock()
        User_mock.return_value = user_mock
        community_social_worker_profile_mock = Mock()
        CommunitySocialWorkerProfile_mock.from_create_user_request\
            .return_value = community_social_worker_profile_mock

        password_hash = b"test_password_hash"
        self.password_util_mock.hash.return_value = password_hash
        user_id = "test_user_id"
        self.users_repository_mock.create.return_value = user_id

        result = self.use_case.create_user(create_user_request_mock)

        assert result == user_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock.principal.user,
            [constants.user_roles.admin]
        )
        self.create_user_request_validation_util_mock.validate.assert_called_once_with(
            create_user_request_mock
        )
        self.password_util_mock.hash.assert_called_once_with(
            create_user_request_mock.password
        )
        CommunitySocialWorkerProfile_mock.from_create_user_request\
            .assert_called_once_with(create_user_request_mock)
        User_mock.assert_called_once_with(
            None,
            create_user_request_mock.role,
            create_user_request_mock.email,
            password_hash,
            None,
            community_social_worker_profile_mock
        )
        self.users_repository_mock.create.assert_called_once_with(user_mock)
        user_mock.on_create.assert_called_once_with(user_id)

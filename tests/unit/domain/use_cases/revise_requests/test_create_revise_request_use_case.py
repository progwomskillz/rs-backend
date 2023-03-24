import pytest
from mock import Mock, patch

from domain.entities.exceptions import (
    InvalidRequest,
    NotFoundException,
    UnauthenticatedException,
    UnauthorizedException
)
from domain.use_cases.revise_requests import CreateReviseRequestUseCase
from domain.utils import constants


class TestCreateReviseRequestUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.rbac_validation_util_mock = Mock()
        self.create_revise_request_request_validation_util_mock = Mock()
        self.revise_requests_repository_mock = Mock()
        self.polls_repository_mock = Mock()

        self.use_case = CreateReviseRequestUseCase(
            self.principal_validation_util_mock,
            self.rbac_validation_util_mock,
            self.create_revise_request_request_validation_util_mock,
            self.revise_requests_repository_mock,
            self.polls_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.rbac_validation_util ==\
            self.rbac_validation_util_mock
        assert self.use_case.create_revise_request_request_validation_util ==\
            self.create_revise_request_request_validation_util_mock
        assert self.use_case.revise_requests_repository ==\
            self.revise_requests_repository_mock
        assert self.use_case.polls_repository ==\
            self.polls_repository_mock

    def test_create_revise_request_invalid_principal(self):
        create_revise_request_request_mock = Mock()
        create_revise_request_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.create_revise_request(create_revise_request_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_not_called()
        self.create_revise_request_request_validation_util_mock.validate.assert_not_called()
        self.revise_requests_repository_mock.create.assert_not_called()
        self.revise_requests_repository_mock.find_by_id.assert_not_called()

    def test_create_revise_request_invalid_principal_role(self):
        create_revise_request_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        create_revise_request_request_mock.principal = principal_mock

        self.rbac_validation_util_mock.validate.side_effect = [
            UnauthorizedException()
        ]

        with pytest.raises(UnauthorizedException):
            self.use_case.create_revise_request(create_revise_request_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal.user,
            [constants.user_roles.public_official]
        )
        self.create_revise_request_request_validation_util_mock.validate.assert_not_called()
        self.revise_requests_repository_mock.create.assert_not_called()
        self.revise_requests_repository_mock.find_by_id.assert_not_called()

    def test_create_revise_request_invalid_request(self):
        create_revise_request_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        create_revise_request_request_mock.principal = principal_mock

        self.create_revise_request_request_validation_util_mock.validate.side_effect = [
            InvalidRequest({})
        ]

        with pytest.raises(InvalidRequest):
            self.use_case.create_revise_request(create_revise_request_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal.user,
            [constants.user_roles.public_official]
        )
        self.create_revise_request_request_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock
        )
        self.polls_repository_mock.find_by_id.assert_not_called()
        self.revise_requests_repository_mock.create.assert_not_called()
        self.revise_requests_repository_mock.find_by_id.assert_not_called()

    def test_create_revise_request_poll_not_found(self):
        create_revise_request_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        create_revise_request_request_mock.principal = principal_mock
        create_revise_request_request_mock.poll_id = "test_poll_id"

        self.polls_repository_mock.find_by_id.return_value = None

        with pytest.raises(NotFoundException):
            self.use_case.create_revise_request(create_revise_request_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal.user,
            [constants.user_roles.public_official]
        )
        self.create_revise_request_request_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock
        )
        self.polls_repository_mock.find_by_id.assert_called_once_with(
            create_revise_request_request_mock.poll_id
        )
        self.revise_requests_repository_mock.create.assert_not_called()
        self.revise_requests_repository_mock.find_by_id.assert_not_called()

    @patch("domain.use_cases.revise_requests.create_revise_request_use_case.ReviseRequest")
    def test_create_revise_request(self, ReviseRequest_mock):
        create_revise_request_request_mock = Mock()
        principal_user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = principal_user_mock
        create_revise_request_request_mock.principal = principal_mock
        create_revise_request_request_mock.poll_id = "test_poll_id"

        poll_mock = Mock()
        self.polls_repository_mock.find_by_id.return_value = poll_mock
        revise_request_mock = Mock()
        ReviseRequest_mock.return_value = revise_request_mock

        revise_request_id = "test_revise_request_id"
        self.revise_requests_repository_mock.create.return_value =\
            revise_request_id
        created_revise_request_mock = Mock()
        self.revise_requests_repository_mock.find_by_id.return_value =\
            created_revise_request_mock

        result = self.use_case.create_revise_request(
            create_revise_request_request_mock
        )

        assert result == created_revise_request_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock.principal.user,
            [constants.user_roles.public_official]
        )
        self.create_revise_request_request_validation_util_mock.validate.assert_called_once_with(
            create_revise_request_request_mock
        )
        self.polls_repository_mock.find_by_id.assert_called_once_with(
            create_revise_request_request_mock.poll_id
        )
        ReviseRequest_mock.assert_called_once_with(
            None,
            principal_mock.user,
            poll_mock
        )
        self.revise_requests_repository_mock.create.assert_called_once_with(
            revise_request_mock
        )
        self.revise_requests_repository_mock.find_by_id.assert_called_once_with(
            revise_request_id
        )

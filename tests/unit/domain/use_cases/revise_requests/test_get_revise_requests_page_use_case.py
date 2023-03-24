import pytest
from mock import Mock

from domain.entities.exceptions import (
    InvalidRequest,
    UnauthenticatedException,
    UnauthorizedException
)
from domain.use_cases.revise_requests import GetReviseRequestsPageUseCase
from domain.utils import constants


class TestGetReviseRequestsPageUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.rbac_validation_util_mock = Mock()
        self.get_revise_requests_page_request_validation_util_mock = Mock()
        self.revise_requests_repository_mock = Mock()

        self.use_case = GetReviseRequestsPageUseCase(
            self.principal_validation_util_mock,
            self.rbac_validation_util_mock,
            self.get_revise_requests_page_request_validation_util_mock,
            self.revise_requests_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.rbac_validation_util ==\
            self.rbac_validation_util_mock
        assert self.use_case.get_revise_requests_page_request_validation_util ==\
            self.get_revise_requests_page_request_validation_util_mock
        assert self.use_case.revise_requests_repository ==\
            self.revise_requests_repository_mock

    def test_get_revise_requests_page_invalid_principal(self):
        get_revise_requests_page_request_mock = Mock()
        get_revise_requests_page_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_revise_requests_page(get_revise_requests_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_not_called()
        self.get_revise_requests_page_request_validation_util_mock.validate.assert_not_called()
        self.revise_requests_repository_mock.get_page.assert_not_called()

    def test_get_revise_requests_page_invalid_principal_role(self):
        get_revise_requests_page_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        get_revise_requests_page_request_mock.principal = principal_mock

        self.rbac_validation_util_mock.validate.side_effect = [
            UnauthorizedException()
        ]

        with pytest.raises(UnauthorizedException):
            self.use_case.get_revise_requests_page(get_revise_requests_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.get_revise_requests_page_request_validation_util_mock.validate.assert_not_called()
        self.revise_requests_repository_mock.get_page.assert_not_called()

    def test_get_revise_requests_page_invalid_request(self):
        get_revise_requests_page_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        get_revise_requests_page_request_mock.principal = principal_mock

        self.get_revise_requests_page_request_validation_util_mock.validate.side_effect = [
            InvalidRequest({})
        ]

        with pytest.raises(InvalidRequest):
            self.use_case.get_revise_requests_page(get_revise_requests_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.get_revise_requests_page_request_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock
        )
        self.revise_requests_repository_mock.get_page.assert_not_called()

    def test_get_revise_requests_page(self):
        get_revise_requests_page_request_mock = Mock()
        get_revise_requests_page_request_mock.user_id = None
        get_revise_requests_page_request_mock.page = 1
        get_revise_requests_page_request_mock.page_size = 10
        principal_mock = Mock()
        principal_user_mock = Mock()
        principal_user_mock.role = constants.user_roles.community_social_worker
        principal_mock.user = principal_user_mock
        get_revise_requests_page_request_mock.principal = principal_mock

        revise_requests_page_mock = Mock()
        self.revise_requests_repository_mock.get_page.return_value = revise_requests_page_mock

        result = self.use_case.get_revise_requests_page(get_revise_requests_page_request_mock)

        assert result == revise_requests_page_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.get_revise_requests_page_request_validation_util_mock.validate.assert_called_once_with(
            get_revise_requests_page_request_mock
        )
        self.revise_requests_repository_mock.get_page.assert_called_once_with(
            principal_user_mock.id,
            get_revise_requests_page_request_mock.page,
            get_revise_requests_page_request_mock.page_size
        )

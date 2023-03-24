import pytest
from mock import Mock, patch

from domain.entities.exceptions import (
    InvalidRequest,
    UnauthenticatedException,
    UnauthorizedException
)
from domain.use_cases.polls import GetPollsPageUseCase
from domain.utils import constants
from tests.factories.polls import FeedbackFactory


class TestGetPollsPaageUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.rbac_validation_util_mock = Mock()
        self.get_polls_page_request_validation_util_mock = Mock()
        self.polls_repository_mock = Mock()

        self.use_case = GetPollsPageUseCase(
            self.principal_validation_util_mock,
            self.rbac_validation_util_mock,
            self.get_polls_page_request_validation_util_mock,
            self.polls_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.rbac_validation_util ==\
            self.rbac_validation_util_mock
        assert self.use_case.get_polls_page_request_validation_util ==\
            self.get_polls_page_request_validation_util_mock
        assert self.use_case.polls_repository ==\
            self.polls_repository_mock

    def test_get_polls_page_invalid_principal(self):
        get_polls_page_request_mock = Mock()
        get_polls_page_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_polls_page(get_polls_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_not_called()
        self.get_polls_page_request_validation_util_mock.validate.assert_not_called()
        self.polls_repository_mock.get_page.assert_not_called()

    def test_get_polls_page_invalid_principal_role(self):
        get_polls_page_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        get_polls_page_request_mock.principal = principal_mock

        self.rbac_validation_util_mock.validate.side_effect = [
            UnauthorizedException()
        ]

        with pytest.raises(UnauthorizedException):
            self.use_case.get_polls_page(get_polls_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal.user,
            [
                constants.user_roles.public_official,
                constants.user_roles.community_social_worker
            ]
        )
        self.get_polls_page_request_validation_util_mock.validate.assert_not_called()
        self.polls_repository_mock.get_page.assert_not_called()

    def test_get_polls_page_invalid_request(self):
        get_polls_page_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        get_polls_page_request_mock.principal = principal_mock

        self.get_polls_page_request_validation_util_mock.validate.side_effect = [
            InvalidRequest({})
        ]

        with pytest.raises(InvalidRequest):
            self.use_case.get_polls_page(get_polls_page_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal.user,
            [
                constants.user_roles.public_official,
                constants.user_roles.community_social_worker
            ]
        )
        self.get_polls_page_request_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock
        )
        self.polls_repository_mock.get_page.assert_not_called()

    def test_get_polls_page_public_official(self):
        get_polls_page_request_mock = Mock()
        get_polls_page_request_mock.user_id = None
        get_polls_page_request_mock.page = 1
        get_polls_page_request_mock.page_size = 10
        principal_mock = Mock()
        principal_user_mock = Mock()
        principal_user_mock.role = constants.user_roles.public_official
        principal_mock.user = principal_user_mock
        get_polls_page_request_mock.principal = principal_mock

        polls_page_mock = Mock()
        self.polls_repository_mock.get_page.return_value = polls_page_mock

        result = self.use_case.get_polls_page(get_polls_page_request_mock)

        assert result == polls_page_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal.user,
            [
                constants.user_roles.public_official,
                constants.user_roles.community_social_worker
            ]
        )
        self.get_polls_page_request_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock
        )
        self.polls_repository_mock.get_page.assert_called_once_with(
            get_polls_page_request_mock.user_id,
            get_polls_page_request_mock.page,
            get_polls_page_request_mock.page_size
        )

    def test_get_polls_page_community_social_worker(self):
        get_polls_page_request_mock = Mock()
        get_polls_page_request_mock.user_id = None
        get_polls_page_request_mock.page = 1
        get_polls_page_request_mock.page_size = 10
        principal_mock = Mock()
        principal_user_mock = Mock()
        principal_user_mock.role = constants.user_roles.community_social_worker
        principal_mock.user = principal_user_mock
        get_polls_page_request_mock.principal = principal_mock

        polls_page_mock = Mock()
        self.polls_repository_mock.get_page.return_value = polls_page_mock

        result = self.use_case.get_polls_page(get_polls_page_request_mock)

        assert result == polls_page_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock.principal.user,
            [
                constants.user_roles.public_official,
                constants.user_roles.community_social_worker
            ]
        )
        self.get_polls_page_request_validation_util_mock.validate.assert_called_once_with(
            get_polls_page_request_mock
        )
        self.polls_repository_mock.get_page.assert_called_once_with(
            principal_user_mock.id,
            get_polls_page_request_mock.page,
            get_polls_page_request_mock.page_size
        )

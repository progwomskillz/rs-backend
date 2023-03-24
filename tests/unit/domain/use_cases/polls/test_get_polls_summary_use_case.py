import pytest
from mock import Mock

from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException
)
from domain.use_cases.polls import GetPollsSummaryUseCase
from domain.utils import constants


class TestGetPollsSummaryUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.rbac_validation_util_mock = Mock()
        self.polls_repository_mock = Mock()

        self.use_case = GetPollsSummaryUseCase(
            self.principal_validation_util_mock,
            self.rbac_validation_util_mock,
            self.polls_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.rbac_validation_util ==\
            self.rbac_validation_util_mock
        assert self.use_case.polls_repository ==\
            self.polls_repository_mock

    def test_get_polls_summary_invalid_principal(self):
        get_polls_summary_request_mock = Mock()
        get_polls_summary_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_polls_summary(get_polls_summary_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_summary_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_not_called()
        self.polls_repository_mock.get_summary.assert_not_called()

    def test_get_polls_summary_invalid_principal_role(self):
        get_polls_summary_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        get_polls_summary_request_mock.principal = principal_mock

        self.rbac_validation_util_mock.validate.side_effect = [
            UnauthorizedException()
        ]

        with pytest.raises(UnauthorizedException):
            self.use_case.get_polls_summary(get_polls_summary_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_summary_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_polls_summary_request_mock.principal.user,
            [constants.user_roles.public_official]
        )
        self.polls_repository_mock.get_summary.assert_not_called()

    def test_get_polls_summary(self):
        get_polls_summary_request_mock = Mock()
        principal_mock = Mock()
        principal_user_mock = Mock()
        principal_user_mock.role = constants.user_roles.public_official
        principal_mock.user = principal_user_mock
        get_polls_summary_request_mock.principal = principal_mock

        polls_summary_mock = Mock()
        self.polls_repository_mock.get_summary.return_value = polls_summary_mock

        result = self.use_case.get_polls_summary(get_polls_summary_request_mock)

        assert result == polls_summary_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            get_polls_summary_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            get_polls_summary_request_mock.principal.user,
            [constants.user_roles.public_official]
        )
        self.polls_repository_mock.get_summary.assert_called_once_with()

import pytest
from mock import Mock, patch

from domain.entities.exceptions import (
    InvalidRequest,
    UnauthenticatedException,
    UnauthorizedException
)
from domain.use_cases.polls import CreatePollUseCase
from domain.utils import constants
from tests.factories.polls import FeedbackFactory


class TestCreatePollUseCase():
    def setup_method(self):
        self.principal_validation_util_mock = Mock()
        self.rbac_validation_util_mock = Mock()
        self.create_poll_request_validation_util_mock = Mock()
        self.polls_repository_mock = Mock()

        self.use_case = CreatePollUseCase(
            self.principal_validation_util_mock,
            self.rbac_validation_util_mock,
            self.create_poll_request_validation_util_mock,
            self.polls_repository_mock
        )

    def test_init(self):
        assert self.use_case.principal_validation_util ==\
            self.principal_validation_util_mock
        assert self.use_case.rbac_validation_util ==\
            self.rbac_validation_util_mock
        assert self.use_case.create_poll_request_validation_util ==\
            self.create_poll_request_validation_util_mock
        assert self.use_case.polls_repository ==\
            self.polls_repository_mock

    def test_create_poll_invalid_principal(self):
        create_poll_request_mock = Mock()
        create_poll_request_mock.principal = None

        self.principal_validation_util_mock.validate.side_effect = [
            UnauthenticatedException()
        ]

        with pytest.raises(UnauthenticatedException):
            self.use_case.create_poll(create_poll_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_not_called()
        self.create_poll_request_validation_util_mock.validate.assert_not_called()
        self.polls_repository_mock.create.assert_not_called()
        self.polls_repository_mock.find_by_id.assert_not_called()

    def test_create_poll_invalid_principal_role(self):
        create_poll_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        create_poll_request_mock.principal = principal_mock

        self.rbac_validation_util_mock.validate.side_effect = [
            UnauthorizedException()
        ]

        with pytest.raises(UnauthorizedException):
            self.use_case.create_poll(create_poll_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.create_poll_request_validation_util_mock.validate.assert_not_called()
        self.polls_repository_mock.create.assert_not_called()
        self.polls_repository_mock.find_by_id.assert_not_called()

    def test_create_poll_invalid_request(self):
        create_poll_request_mock = Mock()
        user_mock = Mock()
        principal_mock = Mock()
        principal_mock.user = user_mock
        create_poll_request_mock.principal = principal_mock

        self.create_poll_request_validation_util_mock.validate.side_effect = [
            InvalidRequest({})
        ]

        with pytest.raises(InvalidRequest):
            self.use_case.create_poll(create_poll_request_mock)

        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.create_poll_request_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock
        )
        self.polls_repository_mock.create.assert_not_called()
        self.polls_repository_mock.find_by_id.assert_not_called()

    @patch("domain.use_cases.polls.create_poll_use_case.Poll")
    def test_create_poll(self, Poll_mock):
        create_poll_request_mock = Mock()
        create_poll_request_mock.community_name = "test_community_name"
        create_poll_request_mock.community_size = "test_community_size"
        create_poll_request_mock.feedbacks = [
            FeedbackFactory.generic()
            for _ in range(5)
        ]
        principal_mock = Mock()
        principal_user_mock = Mock()
        principal_mock.user = principal_user_mock
        create_poll_request_mock.principal = principal_mock

        poll_mock = Mock()
        Poll_mock.return_value = poll_mock
        poll_id = "test_poll_id"
        self.polls_repository_mock.create.return_value = poll_id
        created_poll_mock = Mock()
        self.polls_repository_mock.find_by_id.return_value = created_poll_mock

        result = self.use_case.create_poll(create_poll_request_mock)

        assert result == created_poll_mock
        self.principal_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock.principal
        )
        self.rbac_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.create_poll_request_validation_util_mock.validate.assert_called_once_with(
            create_poll_request_mock
        )
        Poll_mock.assert_called_once_with(
            None,
            principal_user_mock,
            None,
            create_poll_request_mock.community_name,
            create_poll_request_mock.community_size,
            create_poll_request_mock.feedbacks,
            None
        )
        self.polls_repository_mock.create.assert_called_once_with(poll_mock)
        self.polls_repository_mock.find_by_id.assert_called_once_with(poll_id)

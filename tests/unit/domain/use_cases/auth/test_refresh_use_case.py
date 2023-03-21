import pytest
from mock import Mock, patch

from domain.use_cases.auth import RefreshUseCase
from domain.entities.exceptions import InvalidRequest, UnauthenticatedException


class TestRefreshUseCase():
    def setup_method(self):
        self.refresh_request_validation_util_mock = Mock()
        self.users_repository_mock = Mock()
        self.tokens_util_mock = Mock()

        self.use_case = RefreshUseCase(
            self.refresh_request_validation_util_mock,
            self.users_repository_mock,
            self.tokens_util_mock
        )

    def test_init(self):
        assert self.use_case.refresh_request_validation_util ==\
            self.refresh_request_validation_util_mock
        assert self.use_case.users_repository == self.users_repository_mock
        assert self.use_case.tokens_util == self.tokens_util_mock

    @patch("domain.use_cases.auth.refresh_use_case.sleep")
    def test_refresh_invalid_request(self, sleep_mock):
        refresh_request_mock = Mock()
        refresh_request_mock.refresh = None

        validation_errors = {}
        self.refresh_request_validation_util_mock.validate.side_effect = [
            InvalidRequest(validation_errors)
        ]

        with pytest.raises(InvalidRequest) as e:
            self.use_case.refresh(refresh_request_mock)

        assert e.value.errors == validation_errors

        self.refresh_request_validation_util_mock.validate.assert_called_once_with(
            refresh_request_mock
        )
        self.tokens_util_mock.decode.assert_not_called()
        self.users_repository_mock.find_by_id.assert_not_called()
        sleep_mock.assert_not_called()
        self.tokens_util_mock.create_pair.assert_not_called()
        self.users_repository_mock.update.assert_not_called()

    @patch("domain.use_cases.auth.refresh_use_case.sleep")
    def test_refresh_invalid_token(self, sleep_mock):
        refresh_request_mock = Mock()
        refresh_request_mock.refresh = "test_refresh"

        self.tokens_util_mock.decode.return_value = None

        with pytest.raises(UnauthenticatedException):
            self.use_case.refresh(refresh_request_mock)

        self.refresh_request_validation_util_mock.validate.assert_called_once_with(
            refresh_request_mock
        )
        self.tokens_util_mock.decode.assert_called_once_with(
            refresh_request_mock.refresh
        )
        self.users_repository_mock.find_by_id.assert_not_called()
        sleep_mock.assert_not_called()
        self.tokens_util_mock.create_pair.assert_not_called()
        self.users_repository_mock.update.assert_not_called()

    @patch("domain.use_cases.auth.refresh_use_case.sleep")
    def test_refresh_user_not_found(self, sleep_mock):
        refresh_request_mock = Mock()
        refresh_request_mock.refresh = "test_refresh"

        tokens_payload_mock = Mock()
        tokens_payload_mock.user_id = "test_user_id"
        tokens_payload_mock.user_role = "test_user_role"
        self.tokens_util_mock.decode.return_value = tokens_payload_mock
        self.users_repository_mock.find_by_id.return_value = None

        with pytest.raises(UnauthenticatedException):
            self.use_case.refresh(refresh_request_mock)

        self.refresh_request_validation_util_mock.validate.assert_called_once_with(
            refresh_request_mock
        )
        self.tokens_util_mock.decode.assert_called_once_with(
            refresh_request_mock.refresh
        )
        self.users_repository_mock.find_by_id.assert_called_once_with(
            tokens_payload_mock.user_id
        )
        sleep_mock.assert_not_called()
        self.tokens_util_mock.create_pair.assert_not_called()
        self.users_repository_mock.update.assert_not_called()

    @patch("domain.use_cases.auth.refresh_use_case.sleep")
    def test_refresh_token_not_found(self, sleep_mock):
        refresh_request_mock = Mock()
        refresh_request_mock.refresh = "test_refresh"

        tokens_payload_mock = Mock()
        tokens_payload_mock.user_id = "test_user_id"
        tokens_payload_mock.user_role = "test_user_role"
        self.tokens_util_mock.decode.return_value = tokens_payload_mock
        user_mock = Mock()
        user_mock.tokens_pairs = []
        self.users_repository_mock.find_by_id.return_value = user_mock

        with pytest.raises(UnauthenticatedException):
            self.use_case.refresh(refresh_request_mock)

        self.refresh_request_validation_util_mock.validate.assert_called_once_with(
            refresh_request_mock
        )
        self.tokens_util_mock.decode.assert_called_once_with(
            refresh_request_mock.refresh
        )
        self.users_repository_mock.find_by_id.assert_called_once_with(
            tokens_payload_mock.user_id
        )
        sleep_mock.assert_not_called()
        self.tokens_util_mock.create_pair.assert_not_called()
        self.users_repository_mock.update.assert_not_called()

    @patch("domain.use_cases.auth.refresh_use_case.sleep")
    def test_refresh(self, sleep_mock):
        refresh_request_mock = Mock()
        refresh_request_mock.refresh = "test_refresh"

        tokens_payload_mock = Mock()
        tokens_payload_mock.user_id = "test_user_id"
        tokens_payload_mock.user_role = "test_user_role"
        self.tokens_util_mock.decode.return_value = tokens_payload_mock
        tokens_pair_mock = Mock()
        tokens_pair_mock.access = "test_access"
        tokens_pair_mock.refresh = "test_refresh"
        user_mock = Mock()
        user_mock.tokens_pairs = [tokens_pair_mock]
        self.users_repository_mock.find_by_id.return_value = user_mock
        new_tokens_pair_mock = Mock()
        new_tokens_pair_mock.access = "test_access_new"
        new_tokens_pair_mock.refresh = "test_refresh_new"
        self.tokens_util_mock.create_pair.return_value = new_tokens_pair_mock

        result = self.use_case.refresh(refresh_request_mock)

        assert result == new_tokens_pair_mock
        self.refresh_request_validation_util_mock.validate.assert_called_once_with(
            refresh_request_mock
        )
        self.tokens_util_mock.decode.assert_called_once_with(
            refresh_request_mock.refresh
        )
        self.users_repository_mock.find_by_id.assert_called_once_with(
            tokens_payload_mock.user_id
        )
        sleep_mock.assert_called_once_with(1)
        self.tokens_util_mock.create_pair.assert_called_once_with(
            tokens_payload_mock
        )
        new_tokens_pair_mock.set_refresh.assert_called_once_with(
            refresh_request_mock.refresh
        )
        user_mock.on_refresh.assert_called_once_with(
            new_tokens_pair_mock
        )
        self.users_repository_mock.update.assert_called_once_with(user_mock)

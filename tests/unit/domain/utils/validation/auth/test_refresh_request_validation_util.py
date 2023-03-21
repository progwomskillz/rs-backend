import pytest
from mock import Mock

from domain.utils.validation.auth import RefreshRequestValidationUtil
from domain.entities.exceptions import InvalidRequest


class TestRefreshRequestValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()

        self.validation_util = RefreshRequestValidationUtil(
            self.presence_validator_mock,
            self.string_type_validator_mock
        )

    def test_init(self):
        assert self.validation_util.presence_validator ==\
            self.presence_validator_mock
        assert self.validation_util.string_type_validator ==\
            self.string_type_validator_mock

    def test_validate_invalid(self):
        self.presence_validator_mock.is_valid.return_value = False
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.return_value = False
        self.string_type_validator_mock.error = "string_type_error"

        refresh_request_mock = Mock()
        refresh_request_mock.refresh = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(refresh_request_mock)

        assert e.value.errors == {
            "refresh": ["presence_error", "string_type_error"]
        }
        self.presence_validator_mock.is_valid.assert_called_once_with(
            refresh_request_mock.refresh
        )
        self.string_type_validator_mock.is_valid.assert_called_once_with(
            refresh_request_mock.refresh
        )

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True

        refresh_request_mock = Mock()
        refresh_request_mock.refresh = "test_refresh"

        self.validation_util.validate(refresh_request_mock)

        self.presence_validator_mock.is_valid.assert_called_once_with(
            refresh_request_mock.refresh
        )
        self.string_type_validator_mock.is_valid.assert_called_once_with(
            refresh_request_mock.refresh
        )

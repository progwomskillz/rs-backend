import pytest
from mock import Mock

from domain.utils.validation.auth import LoginRequestValidationUtil
from domain.entities.exceptions import InvalidRequest


class TestLoginRequestValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()
        self.email_format_validator_mock = Mock()

        self.validation_util = LoginRequestValidationUtil(
            self.presence_validator_mock,
            self.string_type_validator_mock,
            self.email_format_validator_mock
        )

    def test_init(self):
        assert self.validation_util.presence_validator ==\
            self.presence_validator_mock
        assert self.validation_util.string_type_validator ==\
            self.string_type_validator_mock
        assert self.validation_util.email_format_validator ==\
            self.email_format_validator_mock

    def test_validate_invalid(self):
        self.presence_validator_mock.is_valid.return_value = False
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.return_value = False
        self.string_type_validator_mock.error = "string_type_error"
        self.email_format_validator_mock.is_valid.return_value = False
        self.email_format_validator_mock.error = "email_format_error"

        login_request_mock = Mock()
        login_request_mock.email = None
        login_request_mock.password = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(login_request_mock)

        assert e.value.errors == {
            "email": [
                "presence_error", "string_type_error", "email_format_error"
            ],
            "password": ["presence_error", "string_type_error"]
        }
        assert self.presence_validator_mock.is_valid.call_count == 2
        self.presence_validator_mock.is_valid.assert_any_call(
            login_request_mock.email
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            login_request_mock.password
        )
        assert self.string_type_validator_mock.is_valid.call_count == 2
        self.string_type_validator_mock.is_valid.assert_any_call(
            login_request_mock.email
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            login_request_mock.password
        )
        self.email_format_validator_mock.is_valid.assert_called_once_with(
            login_request_mock.email
        )

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True
        self.email_format_validator_mock.is_valid.return_value = True

        login_request_mock = Mock()
        login_request_mock.email = "test@example.com"
        login_request_mock.password = "test_password"

        self.validation_util.validate(login_request_mock)

        assert self.presence_validator_mock.is_valid.call_count == 2
        self.presence_validator_mock.is_valid.assert_any_call(
            login_request_mock.email
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            login_request_mock.password
        )
        assert self.string_type_validator_mock.is_valid.call_count == 2
        self.string_type_validator_mock.is_valid.assert_any_call(
            login_request_mock.email
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            login_request_mock.password
        )
        self.email_format_validator_mock.is_valid.assert_called_once_with(
            login_request_mock.email
        )

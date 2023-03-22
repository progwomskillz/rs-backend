import pytest
from mock import Mock

from domain.entities.exceptions import InvalidRequest
from domain.utils.validation.users import CreateUserRequestValidationUtil


class TestCreateUserRequestValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()
        self.roles_entry_validator_mock = Mock()
        self.email_format_validator_mock = Mock()
        self.users_repository_mock = Mock()

        self.validation_util = CreateUserRequestValidationUtil(
            self.presence_validator_mock,
            self.string_type_validator_mock,
            self.roles_entry_validator_mock,
            self.email_format_validator_mock,
            self.users_repository_mock
        )

    def test_init(self):
        assert self.validation_util.presence_validator ==\
            self.presence_validator_mock
        assert self.validation_util.string_type_validator ==\
            self.string_type_validator_mock
        assert self.validation_util.roles_entry_validator ==\
            self.roles_entry_validator_mock
        assert self.validation_util.email_format_validator ==\
            self.email_format_validator_mock
        assert self.validation_util.users_repository ==\
            self.users_repository_mock

    def test_validate_invalid_email(self):
        self.presence_validator_mock.is_valid.return_value = False
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.return_value = False
        self.string_type_validator_mock.error = "string_type_error"
        self.roles_entry_validator_mock.is_valid.return_value = False
        self.roles_entry_validator_mock.error = "roles_entry_error"
        self.email_format_validator_mock.is_valid.return_value = False
        self.email_format_validator_mock.error = "email_format_error"
        user_mock = Mock()
        self.users_repository_mock.find_by_email.return_value = user_mock

        create_user_request_mock = Mock()
        principal_mock = Mock()
        create_user_request_mock.principal = principal_mock
        create_user_request_mock.role = None
        create_user_request_mock.email = None
        create_user_request_mock.password = None
        create_user_request_mock.first_name = None
        create_user_request_mock.last_name = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_user_request_mock)

        assert e.value.errors == {
            "role": [
                "presence_error", "string_type_error", "roles_entry_error"
            ],
            "email": [
                "presence_error",
                "string_type_error",
                "email_format_error",
                {"message": "Must be unique", "code": "unique"}
            ],
            "password": ["presence_error", "string_type_error"],
            "first_name": ["presence_error", "string_type_error"],
            "last_name": ["presence_error", "string_type_error"]
        }
        assert self.presence_validator_mock.is_valid.call_count == 5
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.role
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.email
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.password
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.first_name
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.last_name
        )
        assert self.string_type_validator_mock.is_valid.call_count == 5
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.role
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.email
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.password
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.first_name
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.last_name
        )
        self.roles_entry_validator_mock.is_valid.assert_called_once_with(
            create_user_request_mock.role
        )
        self.email_format_validator_mock.is_valid.assert_called_once_with(
            create_user_request_mock.email
        )
        self.users_repository_mock.find_by_email.assert_not_called()

    def test_validate_invalid(self):
        self.presence_validator_mock.is_valid.side_effect = [
            False,
            True,
            False,
            False,
            False
        ]
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.side_effect = [
            False,
            True,
            False,
            False,
            False
        ]
        self.string_type_validator_mock.error = "string_type_error"
        self.roles_entry_validator_mock.is_valid.return_value = False
        self.roles_entry_validator_mock.error = "roles_entry_error"
        self.email_format_validator_mock.is_valid.return_value = False
        self.email_format_validator_mock.error = "email_format_error"
        user_mock = Mock()
        self.users_repository_mock.find_by_email.return_value = user_mock

        create_user_request_mock = Mock()
        principal_mock = Mock()
        create_user_request_mock.principal = principal_mock
        create_user_request_mock.role = None
        create_user_request_mock.email = None
        create_user_request_mock.password = None
        create_user_request_mock.first_name = None
        create_user_request_mock.last_name = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_user_request_mock)

        assert e.value.errors == {
            "role": [
                "presence_error", "string_type_error", "roles_entry_error"
            ],
            "email": [
                "email_format_error",
                {"message": "Must be unique", "code": "unique"}
            ],
            "password": ["presence_error", "string_type_error"],
            "first_name": ["presence_error", "string_type_error"],
            "last_name": ["presence_error", "string_type_error"]
        }
        assert self.presence_validator_mock.is_valid.call_count == 5
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.role
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.email
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.password
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.first_name
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.last_name
        )
        assert self.string_type_validator_mock.is_valid.call_count == 5
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.role
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.email
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.password
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.first_name
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.last_name
        )
        self.roles_entry_validator_mock.is_valid.assert_called_once_with(
            create_user_request_mock.role
        )
        self.email_format_validator_mock.is_valid.assert_called_once_with(
            create_user_request_mock.email
        )
        self.users_repository_mock.find_by_email.assert_called_once_with(
            create_user_request_mock.email
        )

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True
        self.roles_entry_validator_mock = True
        self.email_format_validator_mock.is_valid.return_value = True
        self.users_repository_mock.find_by_email.return_value = None

        create_user_request_mock = Mock()
        principal_mock = Mock()
        create_user_request_mock.principal = principal_mock
        create_user_request_mock.role = "test_role"
        create_user_request_mock.email = "test@example.com"
        create_user_request_mock.password = "test_password"
        create_user_request_mock.first_name = "test_first_name"
        create_user_request_mock.last_name = "test_last_name"

        self.validation_util.validate(create_user_request_mock)

        assert self.presence_validator_mock.is_valid.call_count == 5
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.role
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.email
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.password
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.first_name
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.last_name
        )
        assert self.string_type_validator_mock.is_valid.call_count == 5
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.role
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.email
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.password
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.first_name
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_user_request_mock.last_name
        )
        self.email_format_validator_mock.is_valid.assert_called_once_with(
            create_user_request_mock.email
        )
        self.users_repository_mock.find_by_email.assert_called_once_with(
            create_user_request_mock.email
        )

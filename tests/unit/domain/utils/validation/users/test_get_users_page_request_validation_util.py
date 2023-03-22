import pytest
from mock import Mock

from domain.entities.exceptions import InvalidRequest
from domain.utils.validation.users import GetUsersPageRequestValidationUtil
from domain.utils import constants


class TestGetUsersPageRequestValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()
        self.admin_roles_entry_validator_mock = Mock()
        self.roles_entry_validators = {
            constants.user_roles.admin: self.admin_roles_entry_validator_mock
        }
        self.int_type_validator_mock = Mock()

        self.validation_util = GetUsersPageRequestValidationUtil(
            self.presence_validator_mock,
            self.string_type_validator_mock,
            self.roles_entry_validators,
            self.int_type_validator_mock
        )

    def test_init(self):
        assert self.validation_util.presence_validator ==\
            self.presence_validator_mock
        assert self.validation_util.string_type_validator ==\
            self.string_type_validator_mock
        assert self.validation_util.roles_entry_validators ==\
            self.roles_entry_validators
        assert self.validation_util.int_type_validator ==\
            self.int_type_validator_mock

    def test_validate_invalid(self):
        self.presence_validator_mock.is_valid.return_value = False
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.return_value = False
        self.string_type_validator_mock.error = "string_type_error"
        self.admin_roles_entry_validator_mock.is_valid.return_value = False
        self.admin_roles_entry_validator_mock.error = "roles_entry_error"
        self.int_type_validator_mock.is_valid.return_value = False
        self.int_type_validator_mock.error = "int_type_error"

        get_users_page_request_mock = Mock()
        principal_mock = Mock()
        user_mock = Mock()
        user_mock.role = constants.user_roles.admin
        principal_mock.user = user_mock
        get_users_page_request_mock.principal = principal_mock

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(get_users_page_request_mock)

        assert e.value.errors == {
            "role": [
                "presence_error", "string_type_error", "roles_entry_error"
            ],
            "page": ["presence_error", "int_type_error"],
            "page_size": ["presence_error", "int_type_error"]
        }
        assert self.presence_validator_mock.is_valid.call_count == 3
        self.presence_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.role
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page_size
        )
        self.string_type_validator_mock.is_valid.assert_called_once_with(
            get_users_page_request_mock.role
        )
        self.admin_roles_entry_validator_mock.is_valid.assert_called_once_with(
            get_users_page_request_mock.role
        )
        assert self.int_type_validator_mock.is_valid.call_count == 2
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page
        )
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page_size
        )

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True
        self.admin_roles_entry_validator_mock.is_valid.return_value = True
        self.int_type_validator_mock.is_valid.return_value = True

        get_users_page_request_mock = Mock()
        principal_mock = Mock()
        user_mock = Mock()
        user_mock.role = constants.user_roles.admin
        principal_mock.user = user_mock
        get_users_page_request_mock.principal = principal_mock

        self.validation_util.validate(get_users_page_request_mock)

        assert self.presence_validator_mock.is_valid.call_count == 3
        self.presence_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.role
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page_size
        )
        self.string_type_validator_mock.is_valid.assert_called_once_with(
            get_users_page_request_mock.role
        )
        self.admin_roles_entry_validator_mock.is_valid.assert_called_once_with(
            get_users_page_request_mock.role
        )
        assert self.int_type_validator_mock.is_valid.call_count == 2
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page
        )
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_users_page_request_mock.page_size
        )

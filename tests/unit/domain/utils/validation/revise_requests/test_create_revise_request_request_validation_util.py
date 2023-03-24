import pytest
from mock import Mock

from domain.entities.exceptions import InvalidRequest
from domain.utils.validation.revise_requests import (
    CreateReviseRequestRequestValidationUtil
)


class TestCreateReviseRequestRequestValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()

        self.validation_util = CreateReviseRequestRequestValidationUtil(
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

        create_revise_request_request_mock = Mock()
        principal_mock = Mock()
        create_revise_request_request_mock.principal = principal_mock
        create_revise_request_request_mock.poll_id = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_revise_request_request_mock)

        assert e.value.errors == {
            "poll_id": ["presence_error", "string_type_error"]
        }
        self.presence_validator_mock.is_valid.assert_called_once_with(
            create_revise_request_request_mock.poll_id
        )
        self.string_type_validator_mock.is_valid.assert_called_once_with(
            create_revise_request_request_mock.poll_id
        )

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True

        create_revise_request_request_mock = Mock()
        principal_mock = Mock()
        create_revise_request_request_mock.principal = principal_mock
        create_revise_request_request_mock.poll_id = "test_poll_id"

        self.validation_util.validate(create_revise_request_request_mock)

        self.presence_validator_mock.is_valid.assert_called_once_with(
            create_revise_request_request_mock.poll_id
        )
        self.string_type_validator_mock.is_valid.assert_called_once_with(
            create_revise_request_request_mock.poll_id
        )

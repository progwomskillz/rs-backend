import pytest
from mock import Mock

from domain.entities.exceptions import InvalidRequest
from domain.utils.validation.polls import GetPollsPageRequestValidationUtil


class TestGetPollsPageRequestValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()
        self.int_type_validator_mock = Mock()

        self.validation_util = GetPollsPageRequestValidationUtil(
            self.presence_validator_mock,
            self.int_type_validator_mock,
        )

    def test_init(self):
        assert self.validation_util.presence_validator ==\
            self.presence_validator_mock
        assert self.validation_util.int_type_validator ==\
            self.int_type_validator_mock

    def test_validate_invalid(self):
        self.presence_validator_mock.is_valid.return_value = False
        self.presence_validator_mock.error = "presence_error"
        self.int_type_validator_mock.is_valid.return_value = False
        self.int_type_validator_mock.error = "int_type_error"

        get_polls_page_request_mock = Mock()
        principal_mock = Mock()
        get_polls_page_request_mock.principal = principal_mock
        get_polls_page_request_mock.page = None
        get_polls_page_request_mock.page_size = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(get_polls_page_request_mock)

        assert e.value.errors == {
            "page": ["presence_error", "int_type_error"],
            "page_size": ["presence_error", "int_type_error"]
        }
        assert self.presence_validator_mock.is_valid.call_count == 2
        self.presence_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page_size
        )
        assert self.int_type_validator_mock.is_valid.call_count == 2
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page
        )
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page_size
        )

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True
        self.int_type_validator_mock.is_valid.return_value = True

        get_polls_page_request_mock = Mock()
        principal_mock = Mock()
        get_polls_page_request_mock.principal = principal_mock
        get_polls_page_request_mock.page = 1
        get_polls_page_request_mock.page_size = 10

        self.validation_util.validate(get_polls_page_request_mock)

        assert self.presence_validator_mock.is_valid.call_count == 2
        self.presence_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page_size
        )
        assert self.int_type_validator_mock.is_valid.call_count == 2
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page
        )
        self.int_type_validator_mock.is_valid.assert_any_call(
            get_polls_page_request_mock.page_size
        )

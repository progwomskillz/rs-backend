import pytest
from mock import Mock

from domain.entities.exceptions import InvalidRequest
from domain.utils.validation.polls import CreatePollRequestValidationUtil


class TestCreatePollRequestValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()
        self.int_type_validator_mock = Mock()
        self.list_type_validator_mock = Mock()

        self.validation_util = CreatePollRequestValidationUtil(
            self.presence_validator_mock,
            self.string_type_validator_mock,
            self.int_type_validator_mock,
            self.list_type_validator_mock
        )

    def test_init(self):
        assert self.validation_util.presence_validator ==\
            self.presence_validator_mock
        assert self.validation_util.string_type_validator ==\
            self.string_type_validator_mock
        assert self.validation_util.int_type_validator ==\
            self.int_type_validator_mock
        assert self.validation_util.list_type_validator ==\
            self.list_type_validator_mock

    def test_validate_invalid_feedbacks(self):
        self.presence_validator_mock.is_valid.return_value = False
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.return_value = False
        self.string_type_validator_mock.error = "string_type_error"
        self.int_type_validator_mock.is_valid.return_value = False
        self.int_type_validator_mock.error = "int_type_error"
        self.list_type_validator_mock.is_valid.return_value = False
        self.list_type_validator_mock.error = "list_type_error"

        create_poll_request_mock = Mock()
        principal_mock = Mock()
        create_poll_request_mock.principal = principal_mock
        create_poll_request_mock.community_name = None
        create_poll_request_mock.community_size = None
        create_poll_request_mock.feedbacks = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_poll_request_mock)

        assert e.value.errors == {
            "community_name": ["presence_error", "string_type_error"],
            "community_size": ["presence_error", "int_type_error"],
            "feedbacks": ["presence_error", "list_type_error"]
        }
        assert self.presence_validator_mock.is_valid.call_count == 3
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_name
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_size
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.feedbacks
        )
        self.string_type_validator_mock.is_valid.assert_called_once_with(
            create_poll_request_mock.community_name
        )
        self.int_type_validator_mock.is_valid.assert_called_once_with(
            create_poll_request_mock.community_size
        )
        self.list_type_validator_mock.is_valid.assert_called_once_with(
            create_poll_request_mock.feedbacks
        )

    def test_validate_invalid(self):
        self.presence_validator_mock.is_valid.side_effect = [
            False,
            False,
            True,
            False,
            False
        ]
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.return_value = False
        self.string_type_validator_mock.error = "string_type_error"
        self.int_type_validator_mock.is_valid.return_value = False
        self.int_type_validator_mock.error = "int_type_error"
        self.list_type_validator_mock.is_valid.return_value = True
        self.list_type_validator_mock.error = "list_type_error"

        create_poll_request_mock = Mock()
        principal_mock = Mock()
        create_poll_request_mock.principal = principal_mock
        create_poll_request_mock.community_name = None
        create_poll_request_mock.community_size = None
        feedback_mock = Mock()
        feedback_mock.bothers = None
        feedback_mock.age = None
        create_poll_request_mock.feedbacks = [feedback_mock]

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_poll_request_mock)

        assert e.value.errors == {
            "community_name": ["presence_error", "string_type_error"],
            "community_size": ["presence_error", "int_type_error"],
            "feedbacks.0.bothers": ["presence_error", "string_type_error"],
            "feedbacks.0.age": ["presence_error", "int_type_error"]
        }
        assert self.presence_validator_mock.is_valid.call_count == 5
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_name
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_size
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.feedbacks
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            feedback_mock.bothers
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            feedback_mock.age
        )
        assert self.string_type_validator_mock.is_valid.call_count == 2
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_name
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            feedback_mock.bothers
        )
        assert self.int_type_validator_mock.is_valid.call_count == 2
        self.int_type_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_size
        )
        self.int_type_validator_mock.is_valid.assert_any_call(
            feedback_mock.age
        )
        self.list_type_validator_mock.is_valid.assert_called_once_with(
            create_poll_request_mock.feedbacks
        )

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True
        self.int_type_validator_mock.is_valid.return_value = True
        self.list_type_validator_mock.is_valid.return_value = True

        create_poll_request_mock = Mock()
        principal_mock = Mock()
        create_poll_request_mock.principal = principal_mock
        create_poll_request_mock.community_name = "test_community_name"
        create_poll_request_mock.community_size = 25
        feedback_mock = Mock()
        feedback_mock.bothers = "test_bothers"
        feedback_mock.age = 18
        create_poll_request_mock.feedbacks = [feedback_mock]

        self.validation_util.validate(create_poll_request_mock)

        assert self.presence_validator_mock.is_valid.call_count == 5
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_name
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_size
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.feedbacks
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            feedback_mock.bothers
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            feedback_mock.age
        )
        assert self.string_type_validator_mock.is_valid.call_count == 2
        self.string_type_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_name
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            feedback_mock.bothers
        )
        assert self.int_type_validator_mock.is_valid.call_count == 2
        self.int_type_validator_mock.is_valid.assert_any_call(
            create_poll_request_mock.community_size
        )
        self.int_type_validator_mock.is_valid.assert_any_call(
            feedback_mock.age
        )
        self.list_type_validator_mock.is_valid.assert_called_once_with(
            create_poll_request_mock.feedbacks
        )

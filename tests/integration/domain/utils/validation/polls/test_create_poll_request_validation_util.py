import pytest

from application.structure import structure
from domain.entities.exceptions import InvalidRequest
from domain.entities.polls.requests import CreatePollRequest
from domain.utils.validation.validators import (
    PresenceValidator,
    TypeValidator
)
from domain.utils import constants
from tests.factories.polls import FeedbackFactory


class TestCreatePollRequestValidationUtil():
    def setup_method(self):
        self.validation_util = structure.create_poll_request_validation_util

    def test_init(self):
        assert isinstance(
            self.validation_util.presence_validator,
            PresenceValidator
        ) is True
        assert isinstance(
            self.validation_util.string_type_validator,
            TypeValidator
        ) is True
        assert self.validation_util.string_type_validator.type == str
        assert self.validation_util.string_type_validator.string_type_presentation\
            == "string"
        assert isinstance(
            self.validation_util.int_type_validator,
            TypeValidator
        ) is True
        assert self.validation_util.int_type_validator.type == int
        assert self.validation_util.int_type_validator.string_type_presentation\
            == "integer"
        assert isinstance(
            self.validation_util.list_type_validator,
            TypeValidator
        ) is True
        assert self.validation_util.list_type_validator.type == list
        assert self.validation_util.list_type_validator.string_type_presentation\
            == "array"

    def test_validate_invalid(self):
        create_poll_request = CreatePollRequest(
            None,
            None,
            None,
            None
        )

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_poll_request)

        assert e.value.errors == {
            "community_name": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ],
            "community_size": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ],
            "feedbacks": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"array\"",
                    "code": "type"
                }
            ]
        }

    def test_validate(self):
        create_poll_request = CreatePollRequest(
            None,
            "test_community_name",
            25,
            [FeedbackFactory.generic()]
        )

        self.validation_util.validate(create_poll_request)

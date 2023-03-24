import pytest

from application.structure import structure
from domain.entities.exceptions import InvalidRequest
from domain.entities.revise_requests.requests import CreateReviseRequestRequest
from domain.utils.validation.validators import (
    PresenceValidator,
    TypeValidator
)
from domain.utils import constants


class TestCreateReviseRequestRequestValidationUtil():
    def setup_method(self):
        self.validation_util = structure.create_revise_request_request_validation_util

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

    def test_validate_invalid(self):
        create_revise_request_request = CreateReviseRequestRequest(None, None)

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_revise_request_request)

        assert e.value.errors == {
            "poll_id": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ]
        }

    def test_validate(self):
        create_revise_request_request = CreateReviseRequestRequest(
            None,
            "test_poll_id"
        )

        self.validation_util.validate(create_revise_request_request)

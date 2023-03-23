import pytest

from application.structure import structure
from domain.entities.auth.requests import LoginRequest
from domain.entities.exceptions import InvalidRequest
from domain.utils.validation.validators import (
    PresenceValidator,
    TypeValidator
)


class TestLoginRequestValidationUtil():
    def setup_method(self):
        self.validation_util = structure.login_request_validation_util

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
        login_request = LoginRequest(None, None)

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(login_request)

        assert e.value.errors == {
            "username": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ],
            "password": [
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
        login_request = LoginRequest("test@example.com", "test_password")

        self.validation_util.validate(login_request)

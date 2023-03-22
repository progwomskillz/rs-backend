import pytest

from application.structure import structure
from domain.entities.exceptions import InvalidRequest
from domain.entities.users.requests import CreateUserRequest
from domain.utils.validation.validators import (
    EmailFormatValidator,
    EntryValidator,
    PresenceValidator,
    TypeValidator
)
from domain.utils import constants


class TestCreateUserRequestValidationUtil():
    def setup_method(self):
        self.validation_util = structure.create_user_request_validation_util

        self.roles_possible_values = [
            constants.user_roles.community_social_worker,
            constants.user_roles.public_official
        ]

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
            self.validation_util.roles_entry_validator,
            EntryValidator
        ) is True
        assert self.validation_util.roles_entry_validator.possible_values ==\
            self.roles_possible_values
        assert self.validation_util.roles_entry_validator\
            .possible_values_presentation == f"{self.roles_possible_values}"
        assert isinstance(
            self.validation_util.email_format_validator,
            EmailFormatValidator
        ) is True

    def test_validate_invalid(self):
        create_user_request = CreateUserRequest(
            None,
            None,
            None,
            None,
            None,
            None
        )

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(create_user_request)

        assert e.value.errors == {
            "role": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                },
                {
                    "message": f"Must be in \"{self.roles_possible_values}\"",
                    "code": "entry"
                }
            ],
            "email": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                },
                {
                    "message": "Must be \"*@*\" format without any whitespaces",
                    "code": "email_format"
                },
                {
                    "message": "Must be unique",
                    "code": "unique"
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
            ],
            "first_name": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ],
            "last_name": [
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
        create_user_request = CreateUserRequest(
            None,
            constants.user_roles.community_social_worker,
            "test@example.com",
            "test_password",
            "test_first_name",
            "test_last_name"
        )

        self.validation_util.validate(create_user_request)

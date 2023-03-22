import pytest

from application.structure import structure
from domain.entities.auth import Principal
from domain.entities.exceptions import InvalidRequest
from domain.entities.users.requests import GetUsersPageRequest
from domain.utils.validation.validators import (
    EntryValidator,
    PresenceValidator,
    TypeValidator
)
from domain.utils import constants
from tests.factories.users import UserFactory


class TestGetUsersPageRequestValidationUtil():
    def setup_method(self):
        self.validation_util = structure.get_users_page_request_validation_util

        self.admin_roles_possible_values = [
            constants.user_roles.community_social_worker,
            constants.user_roles.public_official
        ]
        self.public_official_roles_possible_values = [
            constants.user_roles.community_social_worker
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
        assert self.validation_util.string_type_validator\
            .string_type_presentation == "string"
        assert isinstance(
            self.validation_util.roles_entry_validators,
            dict
        ) is True
        assert list(self.validation_util.roles_entry_validators.keys()) == [
            constants.user_roles.admin,
            constants.user_roles.public_official
        ]
        admin_roles_entry_validator =\
            self.validation_util.roles_entry_validators[constants.user_roles.admin]
        assert isinstance(admin_roles_entry_validator, EntryValidator) is True
        assert admin_roles_entry_validator.possible_values ==\
            self.admin_roles_possible_values
        assert admin_roles_entry_validator\
            .possible_values_presentation == f"{self.admin_roles_possible_values}"
        public_official_roles_entry_validator =\
            self.validation_util.roles_entry_validators[constants.user_roles.public_official]
        assert isinstance(public_official_roles_entry_validator, EntryValidator) is True
        assert public_official_roles_entry_validator.possible_values ==\
            self.public_official_roles_possible_values
        assert public_official_roles_entry_validator\
            .possible_values_presentation == f"{self.public_official_roles_possible_values}"
        assert isinstance(
            self.validation_util.int_type_validator,
            TypeValidator
        ) is True
        assert self.validation_util.int_type_validator.type == int
        assert self.validation_util.int_type_validator\
            .string_type_presentation == "integer"

    def test_validate_invalid(self):
        user = UserFactory.admin()
        principal = Principal(user, None)
        get_users_page_request = GetUsersPageRequest(
            principal,
            None,
            None,
            None
        )

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(get_users_page_request)

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
                    "message": f"Must be in \"{self.admin_roles_possible_values}\"",
                    "code": "entry"
                }
            ],
            "page": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ],
            "page_size": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ]
        }

        user = UserFactory.public_official()
        principal = Principal(user, None)
        get_users_page_request = GetUsersPageRequest(
            principal,
            None,
            None,
            None
        )

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(get_users_page_request)

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
                    "message": f"Must be in \"{self.public_official_roles_possible_values}\"",
                    "code": "entry"
                }
            ],
            "page": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ],
            "page_size": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"integer\"",
                    "code": "type"
                }
            ]
        }

    def test_validate(self):
        user = UserFactory.admin()
        principal = Principal(user, None)
        get_users_page_request = GetUsersPageRequest(
            principal,
            constants.user_roles.community_social_worker,
            1,
            10
        )

        self.validation_util.validate(get_users_page_request)

        user = UserFactory.admin()
        principal = Principal(user, None)
        get_users_page_request = GetUsersPageRequest(
            principal,
            constants.user_roles.public_official,
            1,
            10
        )

        self.validation_util.validate(get_users_page_request)

        user = UserFactory.public_official()
        principal = Principal(user, None)
        get_users_page_request = GetUsersPageRequest(
            principal,
            constants.user_roles.community_social_worker,
            1,
            10
        )

        self.validation_util.validate(get_users_page_request)

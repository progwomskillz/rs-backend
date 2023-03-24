import pytest

from application.structure import structure
from domain.entities.auth import Principal
from domain.entities.exceptions import InvalidRequest
from domain.entities.polls.requests import GetPollsPageRequest
from domain.utils.validation.validators import (
    PresenceValidator,
    TypeValidator
)
from tests.factories.users import UserFactory


class TestGetPollsPageRequestValidationUtil():
    def setup_method(self):
        self.validation_util = structure.get_polls_page_request_validation_util

    def test_init(self):
        assert isinstance(
            self.validation_util.presence_validator,
            PresenceValidator
        ) is True
        assert isinstance(
            self.validation_util.int_type_validator,
            TypeValidator
        ) is True
        assert self.validation_util.int_type_validator.type == int
        assert self.validation_util.int_type_validator\
            .string_type_presentation == "integer"

    def test_validate_invalid(self):
        user = UserFactory.public_official()
        principal = Principal(user, None)
        get_polls_page_request = GetPollsPageRequest(
            principal,
            None,
            None
        )

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(get_polls_page_request)

        assert e.value.errors == {
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
        user = UserFactory.public_official()
        principal = Principal(user, None)
        get_polls_page_request = GetPollsPageRequest(
            principal,
            1,
            10
        )

        self.validation_util.validate(get_polls_page_request)

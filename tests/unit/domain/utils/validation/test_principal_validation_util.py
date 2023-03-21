import pytest
from mock import Mock

from domain.entities.exceptions import UnauthenticatedException
from domain.utils.validation import PrincipalValidationUtil


class TestPrincipalValidationUtil():
    def setup_method(self):
        self.util = PrincipalValidationUtil()

    def test_validate_invalid(self):
        principal = None

        with pytest.raises(UnauthenticatedException):
            self.util.validate(principal)

    def test_validate(self):
        principal_mock = Mock()

        self.util.validate(principal_mock)

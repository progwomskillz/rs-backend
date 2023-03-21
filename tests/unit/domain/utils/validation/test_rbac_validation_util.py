import pytest

from domain.entities.exceptions import UnauthorizedException
from domain.utils.validation import RBACValidationUtil
from tests.factories.users import UserFactory


class TestRBAClValidationUtil():
    def setup_method(self):
        self.util = RBACValidationUtil()

    def test_validate_invalid(self):
        user = UserFactory.admin()
        roles = [f"{user.role}_wrong"]

        with pytest.raises(UnauthorizedException):
            self.util.validate(user, roles)

    def test_validate(self):
        user = UserFactory.admin()
        roles = [user.role, f"{user.role}_wrong"]

        self.util.validate(user, roles)

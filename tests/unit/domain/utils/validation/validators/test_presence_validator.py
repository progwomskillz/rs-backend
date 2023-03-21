from domain.utils.validation.validators import PresenceValidator


class TestPresenceValidator():
    def setup_method(self):
        self.validator = PresenceValidator()

    def test_is_valid_none(self):
        result = self.validator.is_valid(None)

        assert result is False

    def test_is_valid_not_none(self):
        result = self.validator.is_valid("test@example.com")

        assert result is True

    def test_error(self):
        result = self.validator.error

        assert result == {
            "message": "Has to be present",
            "code": "presence"
        }

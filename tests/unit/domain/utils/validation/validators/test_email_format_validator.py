from domain.utils.validation.validators import EmailFormatValidator


class TestEmailFormatValidator():
    def setup_method(self):
        self.validator = EmailFormatValidator()

    def test_is_valid_not_str(self):
        result = self.validator.is_valid(123)

        assert result is False

    def test_is_valid_with_whitespaces(self):
        result = self.validator.is_valid("test @ example.com")

        assert result is False

    def test_is_valid_match_re(self):
        result = self.validator.is_valid("test@example.com")

        assert result is True

    def test_is_valid_not_match_re(self):
        result = self.validator.is_valid("email")

        assert result is False

    def test_error(self):
        result = self.validator.error

        assert result == {
            "message": "Must be \"*@*\" format without any whitespaces",
            "code": "email_format"
        }

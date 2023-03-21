from domain.utils.validation.validators import TypeValidator


class TestTypeValidator():
    def setup_method(self):
        self.type = str
        self.string_type_presentation = "string"

        self.validator = TypeValidator(self.type, self.string_type_presentation)

    def test_init(self):
        assert self.validator.type == self.type
        assert self.validator.string_type_presentation ==\
            self.string_type_presentation

    def test_is_valid_another_type(self):
        result = self.validator.is_valid(123)

        assert result is False

    def test_is_valid(self):
        result = self.validator.is_valid("test@example.com")

        assert result is True

    def test_error(self):
        result = self.validator.error

        assert result == {
            "message": f"Must be of type \"{self.string_type_presentation}\"",
            "code": "type"
        }

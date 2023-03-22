from domain.utils.validation.validators import EntryValidator


class TestEntryValidator():
    def setup_method(self):
        self.possible_values = ["test"]
        self.possible_values_presentation = f"{self.possible_values}"

        self.validator = EntryValidator(
            self.possible_values,
            self.possible_values_presentation
        )

    def test_init(self):
        assert self.validator.possible_values == self.possible_values
        assert self.validator.possible_values_presentation ==\
            self.possible_values_presentation

    def test_is_valid_not_in(self):
        result = self.validator.is_valid(123)

        assert result is False

    def test_is_valid(self):
        result = self.validator.is_valid(self.possible_values[0])

        assert result is True

    def test_error(self):
        result = self.validator.error

        assert result == {
            "message": f"Must be in \"{self.possible_values_presentation}\"",
            "code": "entry"
        }

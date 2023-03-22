class EntryValidator():
    def __init__(self, possible_values, possible_values_presentation):
        self.possible_values = possible_values
        self.possible_values_presentation = possible_values_presentation

    def is_valid(self, value):
        return value in self.possible_values

    @property
    def error(self):
        return {
            "message": f"Must be in \"{self.possible_values_presentation}\"",
            "code": "entry"
        }

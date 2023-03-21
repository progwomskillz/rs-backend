class TypeValidator():
    def __init__(self, type, string_type_presentation):
        self.type = type
        self.string_type_presentation = string_type_presentation

    def is_valid(self, value):
        return isinstance(value, self.type)

    @property
    def error(self):
        return {
            "message": f"Must be of type \"{self.string_type_presentation}\"",
            "code": "type"
        }

import re


class EmailFormatValidator():
    def is_valid(self, value):
        if not isinstance(value, str):
            return False
        if len(re.findall(r"[\s]", value)):  # Check for whitespaces
            return False
        if re.match(r"^[^@]+@[^@]+$", value):
            return True
        return False

    @property
    def error(self):
        return {
            "message": "Must be \"*@*\" format without any whitespaces",
            "code": "email_format"
        }

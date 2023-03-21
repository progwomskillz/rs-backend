class PresenceValidator():
    def is_valid(self, value):
        return value is not None

    @property
    def error(self):
        return {
            "message": "Has to be present",
            "code": "presence"
        }

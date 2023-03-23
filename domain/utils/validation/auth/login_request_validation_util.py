from ..base_validation_util import BaseValidationUtil


class LoginRequestValidationUtil(BaseValidationUtil):
    def __init__(self, presence_validator, string_type_validator):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator

    def validate(self, login_request):
        self.errors = {}
        if not self.presence_validator.is_valid(login_request.username):
            super()._append_error("username", self.presence_validator.error)
        if not self.string_type_validator.is_valid(login_request.username):
            super()._append_error("username", self.string_type_validator.error)
        if not self.presence_validator.is_valid(login_request.password):
            super()._append_error("password", self.presence_validator.error)
        if not self.string_type_validator.is_valid(login_request.password):
            super()._append_error("password", self.string_type_validator.error)
        super()._process_errors()

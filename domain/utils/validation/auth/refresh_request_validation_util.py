from ..base_validation_util import BaseValidationUtil


class RefreshRequestValidationUtil(BaseValidationUtil):
    def __init__(self, presence_validator, string_type_validator):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator

    def validate(self, refresh_request):
        self.errors = {}
        if not self.presence_validator.is_valid(refresh_request.refresh):
            super()._append_error("refresh", self.presence_validator.error)
        if not self.string_type_validator.is_valid(refresh_request.refresh):
            super()._append_error("refresh", self.string_type_validator.error)
        super()._process_errors()

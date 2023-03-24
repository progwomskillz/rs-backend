from ..base_validation_util import BaseValidationUtil


class CreateReviseRequestRequestValidationUtil(BaseValidationUtil):
    def __init__(self, presence_validator, string_type_validator):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator

    def validate(self, create_revise_request_request):
        self.errors = {}
        if not self.presence_validator.is_valid(create_revise_request_request.poll_id):
            super()._append_error("poll_id", self.presence_validator.error)
        if not self.string_type_validator.is_valid(create_revise_request_request.poll_id):
            super()._append_error("poll_id", self.string_type_validator.error)
        super()._process_errors()

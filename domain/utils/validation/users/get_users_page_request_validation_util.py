from ..base_validation_util import BaseValidationUtil


class GetUsersPageRequestValidationUtil(BaseValidationUtil):
    def __init__(
        self, presence_validator, string_type_validator, roles_entry_validators,
        int_type_validator
    ):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator
        self.roles_entry_validators = roles_entry_validators
        self.int_type_validator = int_type_validator

    def validate(self, get_users_page_request):
        self.errors = {}
        if not self.presence_validator.is_valid(get_users_page_request.role):
            super()._append_error("role", self.presence_validator.error)
        if not self.string_type_validator.is_valid(get_users_page_request.role):
            super()._append_error("role", self.string_type_validator.error)
        roles_entry_validator = self.roles_entry_validators[get_users_page_request.principal.user.role]
        if not roles_entry_validator.is_valid(get_users_page_request.role):
            super()._append_error("role", roles_entry_validator.error)
        if not self.presence_validator.is_valid(get_users_page_request.page):
            super()._append_error("page", self.presence_validator.error)
        if not self.int_type_validator.is_valid(get_users_page_request.page):
            super()._append_error("page", self.int_type_validator.error)
        if not self.presence_validator.is_valid(get_users_page_request.page_size):
            super()._append_error("page_size", self.presence_validator.error)
        if not self.int_type_validator.is_valid(get_users_page_request.page_size):
            super()._append_error("page_size", self.int_type_validator.error)
        super()._process_errors()

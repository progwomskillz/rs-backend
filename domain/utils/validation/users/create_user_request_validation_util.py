from ..base_validation_util import BaseValidationUtil


class CreateUserRequestValidationUtil(BaseValidationUtil):
    def __init__(
        self, presence_validator, string_type_validator, roles_entry_validator,
        users_repository
    ):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator
        self.roles_entry_validator = roles_entry_validator
        self.users_repository = users_repository

    def validate(self, create_user_request):
        self.errors = {}
        if not self.presence_validator.is_valid(create_user_request.role):
            super()._append_error("role", self.presence_validator.error)
        if not self.string_type_validator.is_valid(create_user_request.role):
            super()._append_error("role", self.string_type_validator.error)
        if not self.roles_entry_validator.is_valid(create_user_request.role):
            super()._append_error("role", self.roles_entry_validator.error)
        if not self.presence_validator.is_valid(create_user_request.username):
            super()._append_error("username", self.presence_validator.error)
        if not self.string_type_validator.is_valid(create_user_request.username):
            super()._append_error("username", self.string_type_validator.error)
        if self.users_repository.find_by_username(create_user_request.username):
            super()._append_error("username", {"message": "Must be unique", "code": "unique"})
        if not self.presence_validator.is_valid(create_user_request.password):
            super()._append_error("password", self.presence_validator.error)
        if not self.string_type_validator.is_valid(create_user_request.password):
            super()._append_error("password", self.string_type_validator.error)
        if not self.presence_validator.is_valid(create_user_request.first_name):
            super()._append_error("first_name", self.presence_validator.error)
        if not self.string_type_validator.is_valid(create_user_request.first_name):
            super()._append_error("first_name", self.string_type_validator.error)
        if not self.presence_validator.is_valid(create_user_request.last_name):
            super()._append_error("last_name", self.presence_validator.error)
        if not self.string_type_validator.is_valid(create_user_request.last_name):
            super()._append_error("last_name", self.string_type_validator.error)
        super()._process_errors()

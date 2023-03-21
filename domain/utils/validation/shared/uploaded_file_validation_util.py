from domain.utils.validation.base_validation_util import BaseValidationUtil


class UploadedFileValidationUtil(BaseValidationUtil):
    def __init__(
            self, presence_validator, string_type_validator,
            exists_uploaded_file_validator
    ):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator
        self.exists_uploaded_file_validator = exists_uploaded_file_validator

    def validate(self, file):
        self.errors = {}
        if not self.presence_validator.is_valid(file.key):
            super()._append_error("key", self.presence_validator.error)
        if not self.string_type_validator.is_valid(file.key):
            super()._append_error("key", self.string_type_validator.error)
        if not self.exists_uploaded_file_validator.is_valid(file.key):
            super()._append_error("key", self.exists_uploaded_file_validator.error)
        if not self.presence_validator.is_valid(file.filename):
            super()._append_error("filename", self.presence_validator.error)
        if not self.string_type_validator.is_valid(file.filename):
            super()._append_error("filename", self.string_type_validator.error)
        super()._process_errors()

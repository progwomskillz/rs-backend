from ..base_validation_util import BaseValidationUtil


class GetPollsPageRequestValidationUtil(BaseValidationUtil):
    def __init__(
        self, presence_validator, string_type_validator, int_type_validator
    ):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator
        self.int_type_validator = int_type_validator

    def validate(self, get_polls_page_request):
        self.errors = {}
        if (
            get_polls_page_request.user_id is not None and
            not self.string_type_validator.is_valid(get_polls_page_request.user_id)
        ):
            super()._append_error("user_id", self.string_type_validator.error)
        if not self.presence_validator.is_valid(get_polls_page_request.page):
            super()._append_error("page", self.presence_validator.error)
        if not self.int_type_validator.is_valid(get_polls_page_request.page):
            super()._append_error("page", self.int_type_validator.error)
        if not self.presence_validator.is_valid(get_polls_page_request.page_size):
            super()._append_error("page_size", self.presence_validator.error)
        if not self.int_type_validator.is_valid(get_polls_page_request.page_size):
            super()._append_error("page_size", self.int_type_validator.error)
        super()._process_errors()

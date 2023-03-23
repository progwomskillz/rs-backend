from ..base_validation_util import BaseValidationUtil


class CreatePollRequestValidationUtil(BaseValidationUtil):
    def __init__(
        self, presence_validator, string_type_validator, int_type_validator,
        list_type_validator
    ):
        self.presence_validator = presence_validator
        self.string_type_validator = string_type_validator
        self.int_type_validator = int_type_validator
        self.list_type_validator = list_type_validator

    def validate(self, create_poll_request):
        self.errors = {}
        if not self.presence_validator.is_valid(create_poll_request.community_name):
            super()._append_error("community_name", self.presence_validator.error)
        if not self.string_type_validator.is_valid(create_poll_request.community_name):
            super()._append_error("community_name", self.string_type_validator.error)
        if not self.presence_validator.is_valid(create_poll_request.community_size):
            super()._append_error("community_size", self.presence_validator.error)
        if not self.int_type_validator.is_valid(create_poll_request.community_size):
            super()._append_error("community_size", self.int_type_validator.error)
        if not self.presence_validator.is_valid(create_poll_request.feedbacks):
            super()._append_error("feedbacks", self.presence_validator.error)
        is_feedbacks_list = True
        if not self.list_type_validator.is_valid(create_poll_request.feedbacks):
            super()._append_error("feedbacks", self.list_type_validator.error)
            is_feedbacks_list = False
        if is_feedbacks_list:
            self.__validate_feedbacks(create_poll_request.feedbacks)
        super()._process_errors()

    def __validate_feedbacks(self, feedbacks):
        for i, feedback in enumerate(feedbacks):
            self.__validate_feedback(feedback, i)

    def __validate_feedback(self, feedback, index):
        if not self.presence_validator.is_valid(feedback.bothers):
            super()._append_error(f"feedbacks.{index}.bothers", self.presence_validator.error)
        if not self.string_type_validator.is_valid(feedback.bothers):
            super()._append_error(f"feedbacks.{index}.bothers", self.string_type_validator.error)
        if not self.presence_validator.is_valid(feedback.age):
            super()._append_error(f"feedbacks.{index}.age", self.presence_validator.error)
        if not self.int_type_validator.is_valid(feedback.age):
            super()._append_error(f"feedbacks.{index}.age", self.int_type_validator.error)

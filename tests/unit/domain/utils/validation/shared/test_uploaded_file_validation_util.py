import pytest
from mock import Mock

from domain.entities.exceptions import InvalidRequest
from domain.utils.validation.shared import UploadedFileValidationUtil


class TestUploadedFileValidationUtil():
    def setup_method(self):
        self.presence_validator_mock = Mock()
        self.string_type_validator_mock = Mock()
        self.exists_uploaded_file_validator_mock = Mock()
        self.validation_util = UploadedFileValidationUtil(
            self.presence_validator_mock,
            self.string_type_validator_mock,
            self.exists_uploaded_file_validator_mock,
        )

    def test_validate_invalid(self):
        self.presence_validator_mock.is_valid.return_value = False
        self.presence_validator_mock.error = "presence_error"
        self.string_type_validator_mock.is_valid.return_value = False
        self.string_type_validator_mock.error = "string_type_error"
        self.exists_uploaded_file_validator_mock.is_valid.return_value = False
        self.exists_uploaded_file_validator_mock.error = "exists_error"

        uploaded_file_mock = Mock()
        uploaded_file_mock.key = None
        uploaded_file_mock.filename = None

        with pytest.raises(InvalidRequest) as e:
            self.validation_util.validate(uploaded_file_mock)

        assert e.value.errors == {
            "key": ["presence_error", "string_type_error", "exists_error"],
            "filename": ["presence_error", "string_type_error"],
        }

    def test_validate(self):
        self.presence_validator_mock.is_valid.return_value = True
        self.string_type_validator_mock.is_valid.return_value = True
        self.exists_uploaded_file_validator_mock.is_valid.return_value = True

        uploaded_file_mock = Mock()
        uploaded_file_mock.key = "test-key"
        uploaded_file_mock.filename = "test-filename"

        self.validation_util.validate(uploaded_file_mock)

        self.presence_validator_mock.is_valid.assert_any_call(
            uploaded_file_mock.key
        )
        self.presence_validator_mock.is_valid.assert_any_call(
            uploaded_file_mock.filename
        )

        self.string_type_validator_mock.is_valid.assert_any_call(
            uploaded_file_mock.key
        )
        self.string_type_validator_mock.is_valid.assert_any_call(
            uploaded_file_mock.filename
        )

        self.exists_uploaded_file_validator_mock.is_valid.assert_any_call(
            uploaded_file_mock.key
        )

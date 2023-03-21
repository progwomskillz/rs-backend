from mock import Mock

from domain.utils.validation.validators import ExistsUploadedFileValidator


class TestExistsUploadedFileValidator():
    def setup_method(self):
        self.s3_wrapper_mock = Mock()
        self.validator = ExistsUploadedFileValidator(self.s3_wrapper_mock)

    def test_is_valid(self):
        value = "test-uploaded-file-key"
        self.s3_wrapper_mock.is_exists.return_value = True

        assert self.validator.is_valid(value)

        self.s3_wrapper_mock.is_exists.assert_called_once_with(value)

    def test_error(self):
        result = self.validator.error

        assert result == {
            "message": "The uploaded file must be existing",
            "code": "exists_uploaded_file"
        }

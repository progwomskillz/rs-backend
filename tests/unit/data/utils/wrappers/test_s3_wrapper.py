from mock import Mock, patch
from botocore.errorfactory import ClientError

from data.utils.wrappers import S3Wrapper
from domain.entities.shared import UploadedFile


class TestS3Wrapper():
    def setup_method(self):
        self.s3_client_mock = Mock()
        self.location = "location"
        self.test_bucket_name = "test_bucket"
        self.key_prefix = "key_prefix"

        self.s3_wrapper = S3Wrapper(
            self.s3_client_mock,
            self.test_bucket_name,
            self.location,
            self.key_prefix
        )

    def test_init(self):
        assert self.s3_wrapper.s3_client == self.s3_client_mock
        assert self.s3_wrapper.bucket_location == self.location
        assert self.s3_wrapper.bucket_name == self.test_bucket_name
        assert self.s3_wrapper.key_prefix == self.key_prefix

    def test_upload_none_file_returns_none(self):
        result = self.s3_wrapper.upload_file(file=None)

        assert result is None

    @patch("data.utils.wrappers.s3_wrapper.Path")
    @patch("data.utils.wrappers.s3_wrapper.uuid")
    def test_upload_file(self, uuid_mock, Path_mock):
        file_mock = Mock()
        file_mock.filename = "test-s3-wrapper-filename"

        path_mock = Mock()
        path_mock.name = f"/{file_mock.filename}"
        Path_mock.return_value = path_mock

        uuid4_value = "test-uuid4-value"
        uuid_mock.uuid4.return_value = uuid4_value
        expected_key_value = f"{self.key_prefix}{uuid4_value}/{path_mock.name}"

        result = self.s3_wrapper.upload_file(file_mock)

        assert isinstance(result, UploadedFile)
        assert result.key == expected_key_value
        assert result.filename == path_mock.name

        self.s3_client_mock.upload_fileobj.assert_called_once_with(
            file_mock,
            self.test_bucket_name,
            expected_key_value
        )
        uuid_mock.uuid4.assert_called_once()
        Path_mock.assert_called_once()

    def test_generate_link_none_key(self):
        result = self.s3_wrapper.generate_link(None)

        assert result is None

    def test_generate_link(self):
        key = "test-key"
        link = "test-link"

        self.s3_client_mock.generate_presigned_url.return_value = link
        result = self.s3_wrapper.generate_link(key)

        assert result == link
        self.s3_client_mock.generate_presigned_url.assert_called_once_with(
            "get_object",
            Params={"Bucket": self.test_bucket_name, "Key": key}
        )

    def test_delete(self):
        key = "test-key"
        self.s3_wrapper.delete(key)

        self.s3_client_mock.delete_object.assert_called_once_with(
            Bucket=self.test_bucket_name,
            Key=key
        )

    def test_delete_raises_client_error(self):
        key = "test-key"

        self.s3_client_mock.delete_object.side_effect = ClientError({}, "test")
        self.s3_wrapper.delete(key)

        self.s3_client_mock.delete_object.assert_called_once_with(
            Bucket=self.test_bucket_name,
            Key=key
        )

    def test_is_exists_none_key(self):
        result = self.s3_wrapper.is_exists(None)

        assert result is False

    def test_is_exists(self):
        key = "test-key"

        result = self.s3_wrapper.is_exists(key)

        assert result is True
        self.s3_client_mock.head_object.assert_called_once_with(
            Bucket=self.test_bucket_name,
            Key=key
        )

    def test_is_exists_client_error(self):
        key = "test-key"

        self.s3_client_mock.head_object.side_effect = ClientError({}, "test")
        result = self.s3_wrapper.is_exists(key)

        assert result is False
        self.s3_client_mock.head_object.assert_called_once_with(
            Bucket=self.test_bucket_name,
            Key=key
        )

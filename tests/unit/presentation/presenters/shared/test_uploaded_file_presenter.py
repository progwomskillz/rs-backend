from mock import Mock

from presentation.presenters.shared import UploadedFilePresenter
from tests.factories.shared import UploadedFileFactory


class TestUploadedFilePresenter():
    def setup_method(self):
        self.s3_wrapper_mock = Mock()
        self.presenter = UploadedFilePresenter(self.s3_wrapper_mock)

    def test_present_none(self):
        result = self.presenter.present(None, None)

        assert result is None

    def test_present(self):
        link = "test-link"
        uploaded_file = UploadedFileFactory.generic()

        self.s3_wrapper_mock.generate_link.return_value = link
        result = self.presenter.present(uploaded_file, principal=None)

        assert result == {
            "key": uploaded_file.key,
            "link": link,
            "filename": uploaded_file.filename
        }
        self.s3_wrapper_mock.generate_link.assert_called_once_with(uploaded_file.key)

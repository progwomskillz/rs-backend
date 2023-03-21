from domain.entities.shared import UploadedFile


class TestUploadedFile():
    def setup_method(self):
        self.key = "test-key"
        self.filename = "test-filename"

    def test_init(self):
        uploaded_file = UploadedFile(self.key, self.filename)

        assert uploaded_file.key == self.key
        assert uploaded_file.filename == self.filename

from data.translators.shared import UploadedFileTranslator
from domain.entities.shared import UploadedFile
from tests.factories.shared import UploadedFileFactory


class TestUploadedFileTranslator():
    def setup_method(self):
        self.translator = UploadedFileTranslator()

    def test_to_document_none_file(self):
        result = self.translator.to_document(None)

        assert result is None

    def test_from_document_none(self):
        result = self.translator.from_document(None)

        assert result is None

    def test_to_document(self):
        uploaded_file = UploadedFileFactory.generic()

        result = self.translator.to_document(uploaded_file)

        assert len(result) == 2
        assert result["key"] == uploaded_file.key
        assert result["filename"] == uploaded_file.filename

    def test_from_document(self):
        document = {
            "key": "test-key",
            "filename": "test-filename",
        }

        result = self.translator.from_document(document)

        assert isinstance(result, UploadedFile)
        assert result.key == document["key"]
        assert result.filename == document["filename"]

from domain.entities.shared import UploadedFile


class UploadedFileFactory:
    @staticmethod
    def generic():
        return UploadedFile("test_key", "test_filename")

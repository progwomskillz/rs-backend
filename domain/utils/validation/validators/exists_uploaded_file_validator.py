class ExistsUploadedFileValidator():
    def __init__(self, s3_wrapper):
        self.s3_wrapper = s3_wrapper

    def is_valid(self, value):
        return self.s3_wrapper.is_exists(value)

    @property
    def error(self):
        return {
            "message": "The uploaded file must be existing",
            "code": "exists_uploaded_file"
        }

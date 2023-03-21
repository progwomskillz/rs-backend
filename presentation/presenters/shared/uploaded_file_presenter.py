class UploadedFilePresenter():
    def __init__(self, s3_wrapper):
        self.s3_wrapper = s3_wrapper

    def present(self, uploaded_file, principal):
        if not uploaded_file:
            return None
        return {
            "key": uploaded_file.key,
            "link": self.s3_wrapper.generate_link(uploaded_file.key),
            "filename": uploaded_file.filename
        }

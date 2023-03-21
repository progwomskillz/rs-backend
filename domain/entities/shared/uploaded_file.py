class UploadedFile():
    def __init__(self, key, filename):
        self.__key = key
        self.__filename = filename

    @property
    def key(self):
        return self.__key

    @property
    def filename(self):
        return self.__filename

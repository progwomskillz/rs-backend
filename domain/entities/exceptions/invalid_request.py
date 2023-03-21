from .base_exception import BaseException


class InvalidRequest(BaseException):
    def __init__(self, errors):
        self.errors = errors

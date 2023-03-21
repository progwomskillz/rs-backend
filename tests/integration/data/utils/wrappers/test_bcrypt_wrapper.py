import os

from application.structure import structure


class TestBcryptWrapper():
    def setup_method(self):
        self.wrapper = structure.bcrypt_wrapper

    def test_init(self):
        assert self.wrapper.complicity == int(os.environ["BCRYPT_COMPLICITY"])

    def test_compare_equal(self):
        password = "test_password"
        password_hash = b"$2b$04$RCo42Ujj0ByRUK9fQVbWzOJP0XmcYc/yRkDheCTL1hFrPGws0.qDi"

        result = self.wrapper.compare(password, password_hash)

        assert result is True

    def test_compare_not_equal(self):
        password = "test_wrong_password"
        password_hash = b"$2b$04$RCo42Ujj0ByRUK9fQVbWzOJP0XmcYc/yRkDheCTL1hFrPGws0.qDi"

        result = self.wrapper.compare(password, password_hash)

        assert result is False

    def test_hash(self):
        password = "test_wrong_password"

        result = self.wrapper.hash(password)

        assert isinstance(result, bytes) is True
        assert self.wrapper.compare(password, result) is True

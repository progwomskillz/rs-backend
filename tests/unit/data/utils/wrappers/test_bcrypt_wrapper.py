from mock import Mock, patch

from data.utils.wrappers import BcryptWrapper


class TestBcryptWrapper():
    def setup_method(self):
        self.complicity = 4

        self.wrapper = BcryptWrapper(self.complicity)

    def test_init(self):
        assert self.wrapper.complicity == self.complicity

    @patch("data.utils.wrappers.bcrypt_wrapper.bcrypt")
    def test_compare_not_equal(self, bcrypt_mock):
        bcrypt_mock.checkpw.return_value = False

        password = "test_password"
        password_hash = b"test_password_hash"

        result = self.wrapper.compare(password, password_hash)

        assert result is False
        bcrypt_mock.checkpw.assert_called_once_with(
            password.encode(),
            password_hash
        )

    @patch("data.utils.wrappers.bcrypt_wrapper.bcrypt")
    def test_compare_equal(self, bcrypt_mock):
        bcrypt_mock.checkpw.return_value = True

        password = "test_password"
        password_hash = b"test_password_hash"

        result = self.wrapper.compare(password, password_hash)

        assert result is True
        bcrypt_mock.checkpw.assert_called_once_with(
            password.encode(),
            password_hash
        )

    @patch("data.utils.wrappers.bcrypt_wrapper.bcrypt")
    def test_hash(self, bcrypt_mock):
        password = "test_password"
        salt_mock = Mock()
        bcrypt_mock.gensalt.return_value = salt_mock
        hash_mock = Mock()
        bcrypt_mock.hashpw.return_value = hash_mock

        result = self.wrapper.hash(password)

        assert result == hash_mock
        bcrypt_mock.gensalt.assert_called_once_with(self.complicity)
        bcrypt_mock.hashpw.assert_called_once_with(
            password.encode(),
            salt_mock
        )

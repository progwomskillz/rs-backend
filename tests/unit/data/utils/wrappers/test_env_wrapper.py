import pytest
from mock import patch

from data.utils.wrappers import EnvWrapper
from domain.entities.exceptions import NotFoundException


class TestEnvWrapper():
    def setup_method(self):
        self.wrapper = EnvWrapper()

    @patch("data.utils.wrappers.env_wrapper.os")
    def test_get_not_found(self, os_mock):
        environ_mock = {}
        os_mock.environ = environ_mock

        key = "test_key"

        with pytest.raises(NotFoundException):
            self.wrapper.get(key)

    @patch("data.utils.wrappers.env_wrapper.os")
    def test_get(self, os_mock):
        key = "test_key"
        value = "test_value"

        environ_mock = {key: value}
        os_mock.environ = environ_mock

        result = self.wrapper.get(key)

        assert result == value

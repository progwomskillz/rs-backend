import os

import pytest

from application.structure import structure
from domain.entities.exceptions import NotFoundException


class TestEnvWrapper():
    def setup_method(self):
        self.wrapper = structure.env_wrapper

    def test_get_not_found(self):
        with pytest.raises(NotFoundException):
            self.wrapper.get("wrong_key")

    def test_get(self):
        key = "APP_NAME"

        result = self.wrapper.get(key)

        assert result == os.environ[key]

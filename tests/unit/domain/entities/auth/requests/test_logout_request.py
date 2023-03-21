from mock import Mock

from domain.entities.auth.requests import LogoutRequest


class TestLogoutRequest():
    def setup_method(self):
        self.principal_mock = Mock()

        self.entity = LogoutRequest(self.principal_mock)

    def test_init(self):
        assert self.entity.principal == self.principal_mock

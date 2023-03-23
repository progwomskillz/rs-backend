from domain.entities.auth.requests import LoginRequest


class TestLoginRequest():
    def setup_method(self):
        self.username = "test_username"
        self.password = "test_password"

        self.entity = LoginRequest(self.username, self.password)

    def test_init(self):
        assert self.entity.username == self.username
        assert self.entity.password == self.password

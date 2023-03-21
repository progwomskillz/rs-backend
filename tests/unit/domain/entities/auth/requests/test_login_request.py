from domain.entities.auth.requests import LoginRequest


class TestLoginRequest():
    def setup_method(self):
        self.email = "test@example.com"
        self.password = "test_password"

        self.entity = LoginRequest(self.email, self.password)

    def test_init(self):
        assert self.entity.email == self.email
        assert self.entity.password == self.password

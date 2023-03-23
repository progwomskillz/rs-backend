from domain.entities.users.requests import CreateUserRequest


class TestCreateUserRequest():
    def setup_method(self):
        self.principal = None
        self.role = "test_role"
        self.username = "test_username"
        self.password = "test_password"
        self.first_name = "test_first_name"
        self.last_name = "test_last_name"

        self.entity = CreateUserRequest(
            self.principal,
            self.role,
            self.username,
            self.password,
            self.first_name,
            self.last_name
        )

    def test_init(self):
        assert self.entity.principal == self.principal
        assert self.entity.role == self.role
        assert self.entity.username == self.username
        assert self.entity.password == self.password
        assert self.entity.first_name == self.first_name
        assert self.entity.last_name == self.last_name

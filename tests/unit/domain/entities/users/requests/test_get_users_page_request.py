from domain.entities.users.requests import GetUsersPageRequest


class TestGetUsersPageRequest():
    def setup_method(self):
        self.principal = None
        self.role = "test_role"
        self.page = 1
        self.page_size = 10

        self.entity = GetUsersPageRequest(
            self.principal,
            self.role,
            self.page,
            self.page_size
        )

    def test_init(self):
        assert self.entity.principal == self.principal
        assert self.entity.role == self.role
        assert self.entity.page == self.page
        assert self.entity.page_size == self.page_size

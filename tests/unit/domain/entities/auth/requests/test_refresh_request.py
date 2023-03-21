from domain.entities.auth.requests import RefreshRequest


class TestRefreshRequest():
    def setup_method(self):
        self.refresh = "test_refresh"

        self.entity = RefreshRequest(self.refresh)

    def test_init(self):
        assert self.entity.refresh == self.refresh

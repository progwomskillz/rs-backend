from domain.entities.auth import TokensPair


class TestTokensPair():
    def setup_method(self):
        self.access = "test_access"
        self.refresh = "test_refresh"

        self.entity = TokensPair(self.access, self.refresh)

    def test_init(self):
        assert self.entity.access == self.access
        assert self.entity.refresh == self.refresh

    def test_set_refresh(self):
        refresh = "test_new_refresh"
        self.entity.set_refresh(refresh)

        assert self.entity.refresh == refresh

from domain.entities.auth import TokensPayload


class TestTokensPayload():
    def setup_method(self):
        self.user_id = "test_user_id"
        self.user_role = "test_user_role"

        self.entity = TokensPayload(self.user_id, self.user_role)

    def test_init(self):
        assert self.entity.user_id == self.user_id
        assert self.entity.user_role == self.user_role

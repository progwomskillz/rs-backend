from domain.entities.auth import Principal
from tests.factories.auth import TokensPairFactory
from tests.factories.users import UserFactory


class TestTokensPair():
    def setup_method(self):
        self.user = UserFactory.admin()
        self.tokens_pair = TokensPairFactory.generic()

        self.entity = Principal(self.user, self.tokens_pair)

    def test_init(self):
        assert self.entity.user == self.user
        assert self.entity.tokens_pair == self.tokens_pair

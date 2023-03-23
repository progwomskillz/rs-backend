from mock import Mock

from domain.entities.users import User


class TestUser():
    def setup_method(self):
        self.id = "test_id"
        self.role = "test_role"
        self.username = "test_username"
        self.password_hash = b"test_password_hash"
        self.tokens_pairs = []
        self.profile_mock = Mock()

        self.entity = User(
            self.id,
            self.role,
            self.username,
            self.password_hash,
            self.tokens_pairs,
            self.profile_mock
        )

    def test_init(self):
        assert self.entity.id == self.id
        assert self.entity.role == self.role
        assert self.entity.username == self.username
        assert self.entity.password_hash == self.password_hash
        assert self.entity.tokens_pairs == self.tokens_pairs
        assert self.entity.profile == self.profile_mock

    def test_on_create(self):
        id = "test_id_new"

        self.entity.on_create(id)

        assert self.entity.id == id

    def test_on_login(self):
        tokens_pair_mock = Mock()

        self.entity.on_login(tokens_pair_mock)

        assert self.entity.tokens_pairs == [
            *self.tokens_pairs,
            tokens_pair_mock
        ]

    def test_on_refresh(self):
        tokens_pair_mock_1 = Mock()
        tokens_pair_mock_1.access = "test_access_1"
        tokens_pair_mock_1.refresh = "test_refresh_1"
        tokens_pair_mock_2 = Mock()
        tokens_pair_mock_2.access = "test_access_2"
        tokens_pair_mock_2.refresh = "test_refresh_2"

        self.entity.on_login(tokens_pair_mock_1)
        self.entity.on_login(tokens_pair_mock_2)

        tokens_pair_mock_1.access = "test_access_3"

        self.entity.on_refresh(tokens_pair_mock_1)

        assert self.entity.tokens_pairs == [
            *self.tokens_pairs,
            tokens_pair_mock_2,
            tokens_pair_mock_1
        ]

    def test_on_logout(self):
        tokens_pair_mock_1 = Mock()
        tokens_pair_mock_1.access = "test_access_1"
        tokens_pair_mock_1.refresh = "test_refresh_1"
        tokens_pair_mock_2 = Mock()
        tokens_pair_mock_2.access = "test_access_2"
        tokens_pair_mock_2.refresh = "test_refresh_2"

        self.entity.on_login(tokens_pair_mock_1)
        self.entity.on_login(tokens_pair_mock_2)

        self.entity.on_logout(tokens_pair_mock_1)

        assert self.entity.tokens_pairs == [
            *self.tokens_pairs,
            tokens_pair_mock_2
        ]

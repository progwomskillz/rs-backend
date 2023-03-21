from mock import Mock

from data.translators.users import UserTranslator
from domain.entities.users import User
from tests.factories.users import UserFactory


class TestUserTranslator():
    def setup_method(self):
        self.tokens_pair_translator_mock = Mock()
        self.admin_profile_translator_mock = Mock()
        self.community_social_worker_profile_translator_mock = Mock()
        self.public_official_profile_translator_mock = Mock()
        self.profile_translators = {
            "admin": self.admin_profile_translator_mock,
            "community_social_worker": self.community_social_worker_profile_translator_mock,
            "public_official": self.public_official_profile_translator_mock
        }

        self.translator = UserTranslator(
            self.tokens_pair_translator_mock,
            self.profile_translators
        )

    def test_init(self):
        assert self.translator.tokens_pair_translator ==\
            self.tokens_pair_translator_mock
        assert self.translator.profile_translators == self.profile_translators

    def test_from_document_admin(self):
        document = {
            "_id": "test_id",
            "role": "admin",
            "email": "test@example.com",
            "password_hash": b"test_password_hash",
            "tokens_pairs": [
                {"access": "test_access_1", "refresh": "test_refresh_1"},
                {"access": "test_access_2", "refresh": "test_refresh_2"}
            ],
            "profile": {
                "first_name": "test_first_name",
                "last_name": "test_last_name"
            }
        }

        tokens_pair_mock_1 = Mock()
        tokens_pair_mock_2 = Mock()
        tokens_pairs_mock = [
            tokens_pair_mock_1,
            tokens_pair_mock_2
        ]
        self.tokens_pair_translator_mock.from_document.side_effect =\
            tokens_pairs_mock
        profile_mock = Mock()
        self.admin_profile_translator_mock.from_document.return_value = profile_mock

        result = self.translator.from_document(document)

        assert isinstance(result, User) is True
        assert result.id == document["_id"]
        assert result.role == document["role"]
        assert result.email == document["email"]
        assert result.password_hash == document["password_hash"]
        assert result.tokens_pairs == tokens_pairs_mock

        assert self.tokens_pair_translator_mock.from_document.call_count == 2
        self.tokens_pair_translator_mock.from_document.assert_any_call(
            document["tokens_pairs"][0]
        )
        self.tokens_pair_translator_mock.from_document.assert_any_call(
            document["tokens_pairs"][1]
        )
        self.admin_profile_translator_mock.from_document\
            .assert_called_once_with(document["profile"])
        self.community_social_worker_profile_translator_mock.from_document\
            .assert_not_called()
        self.public_official_profile_translator_mock.from_document\
            .assert_not_called()

    def test_to_document_admin(self):
        user = UserFactory.admin()
        tokens_pair_mock = Mock()
        user.on_login(tokens_pair_mock)

        tokens_pair_document_mock = Mock()
        self.tokens_pair_translator_mock.to_document.return_value =\
            tokens_pair_document_mock
        profile_mock = Mock()
        self.admin_profile_translator_mock.to_document.return_value =\
            profile_mock

        result = self.translator.to_document(user)

        assert result == {
            "_id": None,
            "role": user.role,
            "email": user.email,
            "password_hash": user.password_hash,
            "tokens_pairs": [tokens_pair_document_mock],
            "profile": profile_mock
        }
        self.tokens_pair_translator_mock.to_document.assert_called_once_with(
            tokens_pair_mock
        )
        self.admin_profile_translator_mock.to_document.assert_called_once_with(
            user.profile
        )
        self.community_social_worker_profile_translator_mock.to_document\
            .assert_not_called()
        self.public_official_profile_translator_mock.to_document\
            .assert_not_called()

    def test_from_document_community_social_worker(self):
        document = {
            "_id": "test_id",
            "role": "community_social_worker",
            "email": "test@example.com",
            "password_hash": b"test_password_hash",
            "tokens_pairs": [
                {"access": "test_access_1", "refresh": "test_refresh_1"},
                {"access": "test_access_2", "refresh": "test_refresh_2"}
            ],
            "profile": {
                "first_name": "test_first_name",
                "last_name": "test_last_name"
            }
        }

        tokens_pair_mock_1 = Mock()
        tokens_pair_mock_2 = Mock()
        tokens_pairs_mock = [
            tokens_pair_mock_1,
            tokens_pair_mock_2
        ]
        self.tokens_pair_translator_mock.from_document.side_effect =\
            tokens_pairs_mock
        profile_mock = Mock()
        self.community_social_worker_profile_translator_mock.from_document\
            .return_value = profile_mock

        result = self.translator.from_document(document)

        assert isinstance(result, User) is True
        assert result.id == document["_id"]
        assert result.role == document["role"]
        assert result.email == document["email"]
        assert result.password_hash == document["password_hash"]
        assert result.tokens_pairs == tokens_pairs_mock

        assert self.tokens_pair_translator_mock.from_document.call_count == 2
        self.tokens_pair_translator_mock.from_document.assert_any_call(
            document["tokens_pairs"][0]
        )
        self.tokens_pair_translator_mock.from_document.assert_any_call(
            document["tokens_pairs"][1]
        )
        self.community_social_worker_profile_translator_mock.from_document\
            .assert_called_once_with(document["profile"])
        self.admin_profile_translator_mock.from_document.assert_not_called()
        self.public_official_profile_translator_mock.from_document\
            .assert_not_called()

    def test_to_document_community_social_worker(self):
        user = UserFactory.community_social_worker()
        tokens_pair_mock = Mock()
        user.on_login(tokens_pair_mock)

        tokens_pair_document_mock = Mock()
        self.tokens_pair_translator_mock.to_document.return_value =\
            tokens_pair_document_mock
        profile_mock = Mock()
        self.community_social_worker_profile_translator_mock.to_document\
            .return_value = profile_mock

        result = self.translator.to_document(user)

        assert result == {
            "_id": None,
            "role": user.role,
            "email": user.email,
            "password_hash": user.password_hash,
            "tokens_pairs": [tokens_pair_document_mock],
            "profile": profile_mock
        }
        self.tokens_pair_translator_mock.to_document.assert_called_once_with(
            tokens_pair_mock
        )
        self.community_social_worker_profile_translator_mock.to_document\
            .assert_called_once_with(user.profile)
        self.admin_profile_translator_mock.to_document.assert_not_called()
        self.public_official_profile_translator_mock.to_document\
            .assert_not_called()

    def test_from_document_public_official(self):
        document = {
            "_id": "test_id",
            "role": "public_official",
            "email": "test@example.com",
            "password_hash": b"test_password_hash",
            "tokens_pairs": [
                {"access": "test_access_1", "refresh": "test_refresh_1"},
                {"access": "test_access_2", "refresh": "test_refresh_2"}
            ],
            "profile": {
                "first_name": "test_first_name",
                "last_name": "test_last_name"
            }
        }

        tokens_pair_mock_1 = Mock()
        tokens_pair_mock_2 = Mock()
        tokens_pairs_mock = [
            tokens_pair_mock_1,
            tokens_pair_mock_2
        ]
        self.tokens_pair_translator_mock.from_document.side_effect =\
            tokens_pairs_mock
        profile_mock = Mock()
        self.public_official_profile_translator_mock.from_document\
            .return_value = profile_mock

        result = self.translator.from_document(document)

        assert isinstance(result, User) is True
        assert result.id == document["_id"]
        assert result.role == document["role"]
        assert result.email == document["email"]
        assert result.password_hash == document["password_hash"]
        assert result.tokens_pairs == tokens_pairs_mock

        assert self.tokens_pair_translator_mock.from_document.call_count == 2
        self.tokens_pair_translator_mock.from_document.assert_any_call(
            document["tokens_pairs"][0]
        )
        self.tokens_pair_translator_mock.from_document.assert_any_call(
            document["tokens_pairs"][1]
        )
        self.public_official_profile_translator_mock.from_document\
            .assert_called_once_with(document["profile"])
        self.admin_profile_translator_mock.from_document.assert_not_called()
        self.community_social_worker_profile_translator_mock.from_document\
            .assert_not_called()

    def test_to_document_public_official(self):
        user = UserFactory.public_official()
        tokens_pair_mock = Mock()
        user.on_login(tokens_pair_mock)

        tokens_pair_document_mock = Mock()
        self.tokens_pair_translator_mock.to_document.return_value =\
            tokens_pair_document_mock
        profile_mock = Mock()
        self.public_official_profile_translator_mock.to_document.return_value =\
            profile_mock

        result = self.translator.to_document(user)

        assert result == {
            "_id": None,
            "role": user.role,
            "email": user.email,
            "password_hash": user.password_hash,
            "tokens_pairs": [tokens_pair_document_mock],
            "profile": profile_mock
        }
        self.tokens_pair_translator_mock.to_document.assert_called_once_with(
            tokens_pair_mock
        )
        self.public_official_profile_translator_mock.to_document\
            .assert_called_once_with(user.profile)
        self.admin_profile_translator_mock.to_document.assert_not_called()
        self.community_social_worker_profile_translator_mock.to_document\
            .assert_not_called()

from application.structure import structure
from data.translators.auth import TokensPairTranslator
from domain.entities.users import User, AdminProfile
from tests.factories.users import UserFactory


class TestUserTranslator():
    def setup_method(self):
        self.translator = structure.user_translator

    def test_init(self):
        assert isinstance(
            self.translator.tokens_pair_translator,
            TokensPairTranslator
        ) is True
        assert isinstance(self.translator.profile_translators, dict) is True

    def test_from_document(self):
        document = {
            "_id": "test_id",
            "role": "admin",
            "email": "test@example.com",
            "password_hash": b"test_password_hash",
            "tokens_pairs": [
                {"access": "test_access", "refresh": "test_refresh"}
            ],
            "profile": {
                "first_name": "test_first_name",
                "last_name": "test_last_name"
            }
        }

        result = self.translator.from_document(document)

        assert isinstance(result, User) is True
        assert result.id == document["_id"]
        assert result.role == document["role"]
        assert result.email == document["email"]
        assert result.password_hash == document["password_hash"]
        assert isinstance(result.tokens_pairs, list) is True
        assert len(result.tokens_pairs) == 1
        assert result.tokens_pairs[0].access == document["tokens_pairs"][0]["access"]
        assert result.tokens_pairs[0].refresh == document["tokens_pairs"][0]["refresh"]
        assert isinstance(result.profile, AdminProfile) is True

    def test_to_document(self):
        user = UserFactory.admin()

        result = self.translator.to_document(user)

        assert result == {
            "_id": None,
            "role": user.role,
            "email": user.email,
            "password_hash": user.password_hash,
            "tokens_pairs": [],
            "profile": {
                "first_name": user.profile.first_name,
                "last_name": user.profile.last_name
            }
        }

from bson import ObjectId

from domain.entities.users import User


class UserTranslator():
    def __init__(self, tokens_pair_translator, profile_translators):
        self.tokens_pair_translator = tokens_pair_translator
        self.profile_translators = profile_translators

    def from_document(self, document):
        profile_translator = self.profile_translators[document["role"]]
        return User(
            str(document.get("_id")),
            document.get("role"),
            document.get("email"),
            document.get("password_hash"),
            [
                self.tokens_pair_translator.from_document(tokens_pair_document)
                for tokens_pair_document in document.get("tokens_pairs", [])
            ],
            profile_translator.from_document(document.get("profile"))
        )

    def to_document(self, user):
        profile_translator = self.profile_translators[user.role]
        return {
            "_id": ObjectId(user.id) if ObjectId.is_valid(user.id) else None,
            "role": user.role,
            "email": user.email,
            "password_hash": user.password_hash,
            "tokens_pairs": [
                self.tokens_pair_translator.to_document(tokens_pair)
                for tokens_pair in user.tokens_pairs
            ],
            "profile": profile_translator.to_document(user.profile)
        }

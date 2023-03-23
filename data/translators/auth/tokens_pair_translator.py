from domain.entities.auth import TokensPair


class TokensPairTranslator():
    def from_document(self, document):
        return TokensPair(
            document.get("access"),
            document.get("refresh")
        )

    def to_document(self, tokens_pair):
        return {
            "access": tokens_pair.access,
            "refresh": tokens_pair.refresh
        }

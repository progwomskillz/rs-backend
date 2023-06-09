from data.translators.auth import TokensPairTranslator
from domain.entities.auth import TokensPair
from tests.factories.auth import TokensPairFactory


class TestTokensPairTranslator():
    def setup_method(self):
        self.translator = TokensPairTranslator()

    def test_from_document(self):
        document = {"access": "test_access", "refresh": "test_refresh"}

        result = self.translator.from_document(document)

        assert isinstance(result, TokensPair) is True
        assert result.access == document["access"]
        assert result.refresh == document["refresh"]

    def test_to_document(self):
        tokens_pair = TokensPairFactory.generic()

        result = self.translator.to_document(tokens_pair)

        assert result == {
            "access": tokens_pair.access,
            "refresh": tokens_pair.refresh
        }

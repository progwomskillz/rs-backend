from domain.entities.auth import TokensPair


class TokensPairFactory():
    @staticmethod
    def generic():
        return TokensPair("test_access", "test_refresh")

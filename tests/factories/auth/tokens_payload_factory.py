from domain.entities.auth import TokensPayload


class TokensPayloadFactory():
    @staticmethod
    def generic():
        return TokensPayload("test_user_id", "test_user_role")

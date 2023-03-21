import os

from application.structure import structure
from domain.entities.auth import TokensPair, TokensPayload
from tests.factories.auth import TokensPayloadFactory


class TestJWTWrapper():
    def setup_method(self):
        self.wrapper = structure.jwt_wrapper

    def test_init(self):
        assert self.wrapper.secret == os.environ["JWT_SECRET"]
        assert self.wrapper.access_ttl == int(os.environ["JWT_ACCESS_TTL"])
        assert self.wrapper.refresh_ttl == int(os.environ["JWT_REFRESH_TTL"])
        assert self.wrapper.algorithm == "HS256"

    def test_create_pair(self):
        tokens_payload = TokensPayloadFactory.generic()

        result = self.wrapper.create_pair(tokens_payload)

        assert isinstance(result, TokensPair) is True
        assert isinstance(result.access, str) is True
        assert len(result.access) > 0
        assert isinstance(result.refresh, str) is True
        assert len(result.refresh) > 0

        decoded_access = self.wrapper.decode(result.access)
        assert isinstance(decoded_access, TokensPayload) is True
        assert decoded_access.user_id == tokens_payload.user_id
        assert decoded_access.user_role == tokens_payload.user_role

        decoded_refresh = self.wrapper.decode(result.refresh)
        assert isinstance(decoded_refresh, TokensPayload) is True
        assert decoded_refresh.user_id == tokens_payload.user_id
        assert decoded_refresh.user_role == tokens_payload.user_role

    def test_decode(self):
        tokens_payload = TokensPayloadFactory.generic()

        tokens_pair = self.wrapper.create_pair(tokens_payload)

        result = self.wrapper.decode(tokens_pair.access)

        assert isinstance(result, TokensPayload) is True
        assert result.user_id == tokens_payload.user_id
        assert result.user_role == tokens_payload.user_role

    def test_decode_invalid(self):
        result = self.wrapper.decode("test_token")

        assert result is None

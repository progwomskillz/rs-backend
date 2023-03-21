from mock import Mock, patch

from data.utils.wrappers import JWTWrapper
from domain.entities.auth import TokensPair, TokensPayload


class TestJWTWrapper():
    def setup_method(self):
        self.secret = "test_secret"
        self.access_ttl = 300
        self.refresh_ttl = 3600

        self.wrapper = JWTWrapper(
            self.secret,
            self.access_ttl,
            self.refresh_ttl
        )

    def test_init(self):
        assert self.wrapper.secret == self.secret
        assert self.wrapper.access_ttl == self.access_ttl
        assert self.wrapper.refresh_ttl == self.refresh_ttl

    @patch("data.utils.wrappers.jwt_wrapper.time")
    @patch("data.utils.wrappers.jwt_wrapper.jwt")
    def test_create_pair(self, jwt_mock, time_mock):
        iat_mock = 1000
        time_mock.time.return_value = iat_mock

        access_mock = "test_access_mock"
        refresh_mock = "test_refresh_mock"
        jwt_mock.encode.side_effect = [access_mock, refresh_mock]

        tokens_payload_mock = Mock()
        tokens_payload_mock.user_id = "test_user_id"
        tokens_payload_mock.user_role = "test_user_role"

        result = self.wrapper.create_pair(tokens_payload_mock)

        assert isinstance(result, TokensPair) is True
        assert result.access == access_mock
        assert result.refresh == refresh_mock
        time_mock.time.assert_called_once()
        assert jwt_mock.encode.call_count == 2
        jwt_mock.encode.assert_any_call(
            {
                "user_id": tokens_payload_mock.user_id,
                "user_role": tokens_payload_mock.user_role,
                "iat": iat_mock,
                "exp": iat_mock + self.access_ttl,
                "purpose": "access"
            },
            self.secret,
            algorithm=self.wrapper.algorithm
        )
        jwt_mock.encode.assert_any_call(
            {
                "user_id": tokens_payload_mock.user_id,
                "user_role": tokens_payload_mock.user_role,
                "iat": iat_mock,
                "exp": iat_mock + self.refresh_ttl,
                "purpose": "refresh"
            },
            self.secret,
            algorithm=self.wrapper.algorithm
        )

    @patch("data.utils.wrappers.jwt_wrapper.jwt")
    def test_decode_invalid(self, jwt_mock):
        jwt_mock.decode.side_effect = [Exception()]

        token = "test_token"

        result = self.wrapper.decode(token)

        assert result is None
        jwt_mock.decode.assert_called_once_with(
            token,
            self.secret,
            algorithms=[self.wrapper.algorithm],
            options={
                "require_exp": True,
                "require_iat": True,
                "verify_exp": True,
                "verify_iat": True
            }
        )

    @patch("data.utils.wrappers.jwt_wrapper.jwt")
    def test_decode(self, jwt_mock):
        decoded_token = {
            "user_id": "test_user_id",
            "user_role": "test_user_role"
        }
        jwt_mock.decode.return_value = decoded_token

        token = "test_token"

        result = self.wrapper.decode(token)

        assert isinstance(result, TokensPayload) is True
        assert result.user_id == decoded_token["user_id"]
        assert result.user_role == decoded_token["user_role"]
        jwt_mock.decode.assert_called_once_with(
            token,
            self.secret,
            algorithms=[self.wrapper.algorithm],
            options={
                "require_exp": True,
                "require_iat": True,
                "verify_exp": True,
                "verify_iat": True
            }
        )

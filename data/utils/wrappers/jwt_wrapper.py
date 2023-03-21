import time

import jwt

from domain.entities.auth import TokensPair, TokensPayload


class JWTWrapper():
    def __init__(self, secret, access_ttl, refresh_ttl):
        self.secret = secret
        self.access_ttl = access_ttl
        self.refresh_ttl = refresh_ttl
        self.algorithm = "HS256"

    def create_pair(self, tokens_payload):
        iat = int(time.time())
        return TokensPair(
            self.__encode(tokens_payload, iat, "access"),
            self.__encode(tokens_payload, iat, "refresh")
        )

    def decode(self, token):
        try:
            decoded_token = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={
                    "require_exp": True,
                    "require_iat": True,
                    "verify_exp": True,
                    "verify_iat": True
                }
            )
        except Exception:
            return None
        tokens_payload = TokensPayload(
            decoded_token["user_id"],
            decoded_token["user_role"]
        )
        return tokens_payload

    def __encode(self, tokens_payload, iat, purpose):
        return jwt.encode(
            {
                "user_id": tokens_payload.user_id,
                "user_role": tokens_payload.user_role,
                "iat": iat,
                "exp": iat + (
                    self.access_ttl
                    if purpose == "access"
                    else self.refresh_ttl
                ),
                "purpose": purpose
            },
            self.secret,
            algorithm=self.algorithm
        )

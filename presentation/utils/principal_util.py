from domain.entities.auth import Principal


class PrincipalUtil():
    def __init__(self, allowed_token_type, tokens_util, users_repository):
        self.allowed_token_type = allowed_token_type.lower()
        self.tokens_util = tokens_util
        self.users_repository = users_repository

    def get(self, authorization_header):
        if not isinstance(authorization_header, str):
            return None
        authorization_header = authorization_header.split(" ")
        if len(authorization_header) != 2:
            return None
        token_type = authorization_header[0].lower()
        if token_type != self.allowed_token_type:
            return None
        token = authorization_header[1]
        tokens_payload = self.tokens_util.decode(token)
        if not tokens_payload:
            return None
        user = self.users_repository.find_by_id(tokens_payload.user_id)
        if not user:
            return None
        current_tokens_pair = None
        for tokens_pair in user.tokens_pairs:
            if tokens_pair.access != token:
                continue
            current_tokens_pair = tokens_pair
            break
        if not current_tokens_pair:
            return None
        return Principal(user, current_tokens_pair)

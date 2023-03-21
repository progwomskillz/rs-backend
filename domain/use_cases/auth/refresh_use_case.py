from time import sleep

from domain.entities.exceptions import UnauthenticatedException


class RefreshUseCase():
    def __init__(
        self, refresh_request_validation_util, users_repository, tokens_util
    ):
        self.refresh_request_validation_util = refresh_request_validation_util
        self.users_repository = users_repository
        self.tokens_util = tokens_util

    def refresh(self, refresh_request):
        self.refresh_request_validation_util.validate(refresh_request)

        tokens_payload = self.tokens_util.decode(refresh_request.refresh)

        if not tokens_payload:
            raise UnauthenticatedException()

        user = self.users_repository.find_by_id(tokens_payload.user_id)

        if not user:
            raise UnauthenticatedException()

        current_tokens_pairs = [
            tokens_pair
            for tokens_pair in user.tokens_pairs
            if tokens_pair.refresh == refresh_request.refresh
        ]
        if not current_tokens_pairs:
            raise UnauthenticatedException()

        sleep(1)
        new_tokens_pair = self.tokens_util.create_pair(tokens_payload)
        new_tokens_pair.set_refresh(refresh_request.refresh)

        user.on_refresh(new_tokens_pair)

        self.users_repository.update(user)

        return new_tokens_pair

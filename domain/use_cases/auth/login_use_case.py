from domain.entities.exceptions import UnauthenticatedException
from domain.entities.auth import TokensPayload


class LoginUseCase():
    def __init__(
        self, login_request_validation_util, users_repository, password_util,
        tokens_util
    ):
        self.login_request_validation_util = login_request_validation_util
        self.users_repository = users_repository
        self.password_util = password_util
        self.tokens_util = tokens_util

    def login(self, login_request):
        self.login_request_validation_util.validate(login_request)

        user = self.users_repository.find_by_email(login_request.email)

        if not user:
            raise UnauthenticatedException()

        if not self.password_util.compare(
            login_request.password,
            user.password_hash
        ):
            raise UnauthenticatedException()

        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = self.tokens_util.create_pair(tokens_payload)
        user.on_login(tokens_pair)

        self.users_repository.update(user)

        return tokens_pair

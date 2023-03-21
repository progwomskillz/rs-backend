class LogoutUseCase():
    def __init__(self, principal_validation_util, users_repository):
        self.principal_validation_util = principal_validation_util
        self.users_repository = users_repository

    def logout(self, logout_request):
        self.principal_validation_util.validate(logout_request.principal)

        logout_request.principal.user.on_logout(
            logout_request.principal.tokens_pair
        )
        self.users_repository.update(logout_request.principal.user)

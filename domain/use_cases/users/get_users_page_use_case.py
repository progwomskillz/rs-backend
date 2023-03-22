from domain.utils import constants


class GetUsersPageUseCase():
    def __init__(
        self, principal_validation_util, rbac_validation_util,
        get_users_page_request_validation_util, users_repository
    ):
        self.principal_validation_util = principal_validation_util
        self.rbac_validation_util = rbac_validation_util
        self.get_users_page_request_validation_util = get_users_page_request_validation_util
        self.users_repository = users_repository

    def get_users_page(self, get_users_page_request):
        self.principal_validation_util.validate(
            get_users_page_request.principal
        )
        self.rbac_validation_util.validate(
            get_users_page_request.principal.user,
            [
                constants.user_roles.admin,
                constants.user_roles.public_official
            ]
        )
        self.get_users_page_request_validation_util.validate(
            get_users_page_request
        )
        return self.users_repository.get_page_by_role(
            get_users_page_request.role,
            get_users_page_request.page,
            get_users_page_request.page_size
        )

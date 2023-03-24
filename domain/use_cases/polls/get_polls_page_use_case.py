from domain.utils import constants


class GetPollsPageUseCase():
    def __init__(
        self, principal_validation_util, rbac_validation_util,
        get_polls_page_request_validation_util, polls_repository
    ):
        self.principal_validation_util = principal_validation_util
        self.rbac_validation_util = rbac_validation_util
        self.get_polls_page_request_validation_util = get_polls_page_request_validation_util
        self.polls_repository = polls_repository

    def get_polls_page(self, get_polls_page_request):
        self.principal_validation_util.validate(
            get_polls_page_request.principal
        )
        self.rbac_validation_util.validate(
            get_polls_page_request.principal.user,
            [
                constants.user_roles.public_official,
                constants.user_roles.community_social_worker
            ]
        )
        self.get_polls_page_request_validation_util.validate(
            get_polls_page_request
        )
        if get_polls_page_request.principal.user.role ==\
            constants.user_roles.community_social_worker:
            get_polls_page_request.user_id =\
                get_polls_page_request.principal.user.id
        return self.polls_repository.get_page(
            get_polls_page_request.user_id,
            get_polls_page_request.page,
            get_polls_page_request.page_size
        )

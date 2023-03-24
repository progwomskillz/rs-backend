from domain.utils import constants


class GetReviseRequestsPageUseCase():
    def __init__(
        self, principal_validation_util, rbac_validation_util,
        get_revise_requests_page_request_validation_util,
        revise_requests_repository
    ):
        self.principal_validation_util = principal_validation_util
        self.rbac_validation_util = rbac_validation_util
        self.get_revise_requests_page_request_validation_util =\
            get_revise_requests_page_request_validation_util
        self.revise_requests_repository = revise_requests_repository

    def get_revise_requests_page(self, get_revise_requests_page_request):
        self.principal_validation_util.validate(
            get_revise_requests_page_request.principal
        )
        self.rbac_validation_util.validate(
            get_revise_requests_page_request.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.get_revise_requests_page_request_validation_util.validate(
            get_revise_requests_page_request
        )
        return self.revise_requests_repository.get_page(
            get_revise_requests_page_request.principal.user.id,
            get_revise_requests_page_request.page,
            get_revise_requests_page_request.page_size
        )

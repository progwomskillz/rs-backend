from domain.utils import constants


class GetPollsSummaryUseCase():
    def __init__(
        self, principal_validation_util, rbac_validation_util,
        polls_repository
    ):
        self.principal_validation_util = principal_validation_util
        self.rbac_validation_util = rbac_validation_util
        self.polls_repository = polls_repository

    def get_polls_summary(self, get_polls_summary_request):
        self.principal_validation_util.validate(
            get_polls_summary_request.principal
        )
        self.rbac_validation_util.validate(
            get_polls_summary_request.principal.user,
            [constants.user_roles.public_official]
        )
        return self.polls_repository.get_summary()

from domain.entities.polls import Poll
from domain.utils import constants


class CreatePollUseCase():
    def __init__(
        self, principal_validation_util, rbac_validation_util,
        create_poll_request_validation_util, polls_repository
    ):
        self.principal_validation_util = principal_validation_util
        self.rbac_validation_util = rbac_validation_util
        self.create_poll_request_validation_util = create_poll_request_validation_util
        self.polls_repository = polls_repository

    def create_poll(self, create_poll_request):
        self.principal_validation_util.validate(create_poll_request.principal)
        self.rbac_validation_util.validate(
            create_poll_request.principal.user,
            [constants.user_roles.community_social_worker]
        )
        self.create_poll_request_validation_util.validate(create_poll_request)
        poll = Poll(
            None,
            create_poll_request.principal.user,
            None,
            create_poll_request.community_name,
            create_poll_request.community_size,
            create_poll_request.feedbacks,
            None
        )
        poll_id = self.polls_repository.create(poll)
        return self.polls_repository.find_by_id(poll_id)

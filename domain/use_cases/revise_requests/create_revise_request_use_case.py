from domain.entities.exceptions import NotFoundException
from domain.entities.revise_requests import ReviseRequest
from domain.utils import constants


class CreateReviseRequestUseCase():
    def __init__(
        self, principal_validation_util, rbac_validation_util,
        create_revise_request_request_validation_util,
        revise_requests_repository, polls_repository
    ):
        self.principal_validation_util = principal_validation_util
        self.rbac_validation_util = rbac_validation_util
        self.create_revise_request_request_validation_util =\
            create_revise_request_request_validation_util
        self.revise_requests_repository = revise_requests_repository
        self.polls_repository = polls_repository

    def create_revise_request(self, create_revise_request_request):
        self.principal_validation_util.validate(
            create_revise_request_request.principal
        )
        self.rbac_validation_util.validate(
            create_revise_request_request.principal.user,
            [constants.user_roles.public_official]
        )
        self.create_revise_request_request_validation_util.validate(
            create_revise_request_request
        )
        poll = self.polls_repository.find_by_id(
            create_revise_request_request.poll_id
        )
        if not poll:
            raise NotFoundException()
        revise_request = ReviseRequest(
            None,
            create_revise_request_request.principal.user,
            poll
        )
        revise_request_id = self.revise_requests_repository.create(
            revise_request
        )
        return self.revise_requests_repository.find_by_id(revise_request_id)

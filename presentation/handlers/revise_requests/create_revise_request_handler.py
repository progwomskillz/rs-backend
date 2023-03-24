from ..auth_base_handler import AuthBaseHandler
from domain.entities.revise_requests.requests import CreateReviseRequestRequest


class CreateReviseRequestHandler(AuthBaseHandler):
    def execute(self, request):
        create_revise_request_request = CreateReviseRequestRequest(
            request.principal,
            request.json.get("poll_id")
        )
        return self.use_case.create_revise_request(
            create_revise_request_request
        )

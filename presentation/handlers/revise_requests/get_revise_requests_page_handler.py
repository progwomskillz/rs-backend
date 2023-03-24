from ..auth_base_handler import AuthBaseHandler
from domain.entities.revise_requests.requests import GetReviseRequestsPageRequest
from domain.utils import TypesHelper


class GetReviseRequestsPageHandler(AuthBaseHandler):
    def execute(self, request):
        get_revise_requests_page_request = GetReviseRequestsPageRequest(
            request.principal,
            TypesHelper.try_to_int(request.args.get("page")),
            TypesHelper.try_to_int(request.args.get("page_size"))
        )
        return self.use_case.get_revise_requests_page(
            get_revise_requests_page_request
        )

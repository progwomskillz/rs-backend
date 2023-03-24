from ..auth_base_handler import AuthBaseHandler
from domain.entities.polls.requests import GetPollsPageRequest
from domain.utils import TypesHelper


class GetPollsPageHandler(AuthBaseHandler):
    def execute(self, request):
        get_polls_page_request = GetPollsPageRequest(
            request.principal,
            TypesHelper.try_to_int(request.args.get("page")),
            TypesHelper.try_to_int(request.args.get("page_size"))
        )
        return self.use_case.get_polls_page(get_polls_page_request)

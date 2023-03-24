from ..auth_base_handler import AuthBaseHandler
from domain.entities.polls.requests import GetPollsSummaryRequest


class GetPollsSummaryHandler(AuthBaseHandler):
    def execute(self, request):
        get_polls_summary_request = GetPollsSummaryRequest(
            request.principal
        )
        return self.use_case.get_polls_summary(get_polls_summary_request)

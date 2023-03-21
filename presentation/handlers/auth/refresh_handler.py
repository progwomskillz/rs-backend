from ..base_handler import BaseHandler
from domain.entities.auth.requests import RefreshRequest


class RefreshHandler(BaseHandler):
    def execute(self, request):
        refresh_request = RefreshRequest(request.json.get("refresh"))
        return self.use_case.refresh(refresh_request)

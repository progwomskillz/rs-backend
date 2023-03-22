from ..auth_base_handler import AuthBaseHandler
from domain.entities.users.requests import GetUsersPageRequest
from domain.utils import TypesHelper


class GetUsersPageHandler(AuthBaseHandler):
    def execute(self, request):
        get_users_page_request = GetUsersPageRequest(
            request.principal,
            request.args.get("role"),
            TypesHelper.try_to_int(request.args.get("page")),
            TypesHelper.try_to_int(request.args.get("page_size"))
        )
        return self.use_case.get_users_page(get_users_page_request)

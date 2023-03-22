from mock import Mock, patch

from presentation.handlers.users import GetUsersPageHandler


class TestGetUsersPageHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter = None
        self.principal_util_mock = Mock()

        self.handler = GetUsersPageHandler(
            self.use_case_mock,
            self.presenter,
            self.principal_util_mock
        )

    @patch("presentation.handlers.users.get_users_page_handler.TypesHelper")
    @patch("presentation.handlers.users.get_users_page_handler.GetUsersPageRequest")
    def test_execute(self, GetUsersPageRequest_mock, TypesHelper_mock):
        get_users_page_request_mock = Mock()
        GetUsersPageRequest_mock.return_value = get_users_page_request_mock
        try_to_int_side_effect = [1, 10]
        TypesHelper_mock.try_to_int.side_effect = try_to_int_side_effect

        request_mock = Mock()
        principal_mock = Mock()
        request_mock.principal = principal_mock
        role = "test_role"
        page = "1"
        page_size = "10"
        request_mock.args = {
            "role": role,
            "page": page,
            "page_size": page_size
        }

        expected_result_mock = Mock()
        self.use_case_mock.get_users_page.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        GetUsersPageRequest_mock.assert_called_once_with(
            principal_mock,
            role,
            try_to_int_side_effect[0],
            try_to_int_side_effect[1]
        )
        assert TypesHelper_mock.try_to_int.call_count == 2
        TypesHelper_mock.try_to_int.assert_any_call(
            request_mock.args.get("page")
        )
        TypesHelper_mock.try_to_int.assert_any_call(
            request_mock.args.get("page_size")
        )
        self.use_case_mock.get_users_page.assert_called_once_with(
            get_users_page_request_mock
        )

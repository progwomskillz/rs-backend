from mock import Mock, patch

from presentation.handlers.auth import LogoutHandler


class TestLogoutHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter = None
        self.principal_util_mock = Mock()

        self.handler = LogoutHandler(
            self.use_case_mock,
            self.presenter,
            self.principal_util_mock
        )

    @patch("presentation.handlers.auth.logout_handler.LogoutRequest")
    def test_execute(self, LogoutRequest):
        logout_request_mock = Mock()
        LogoutRequest.return_value = logout_request_mock

        request_mock = Mock()
        principal_mock = Mock()
        request_mock.principal = principal_mock

        expected_result_mock = Mock()
        self.use_case_mock.logout.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        LogoutRequest.assert_called_once_with(principal_mock)
        self.use_case_mock.logout.assert_called_once_with(logout_request_mock)

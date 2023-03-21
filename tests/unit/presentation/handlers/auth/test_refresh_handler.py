from mock import Mock, patch

from presentation.handlers.auth import RefreshHandler


class TestRefreshHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter_mock = Mock()

        self.handler = RefreshHandler(self.use_case_mock, self.presenter_mock)

    @patch("presentation.handlers.auth.refresh_handler.RefreshRequest")
    def test_execute(self, RefreshRequest_mock):
        refresh_request_mock = Mock()
        RefreshRequest_mock.return_value = refresh_request_mock

        json_mock = Mock()
        refresh = "test@example.com"
        json_mock.get.side_effect = [refresh]
        request_mock = Mock()
        request_mock.json = json_mock

        expected_result_mock = Mock()
        self.use_case_mock.refresh.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        json_mock.get.assert_called_once_with("refresh")
        RefreshRequest_mock.assert_called_once_with(refresh)
        self.use_case_mock.refresh.assert_called_once_with(refresh_request_mock)

from mock import Mock, patch

from presentation.handlers.polls import GetPollsSummaryHandler


class TestGetPollsSummaryHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter = None
        self.principal_util_mock = Mock()

        self.handler = GetPollsSummaryHandler(
            self.use_case_mock,
            self.presenter,
            self.principal_util_mock
        )

    @patch("presentation.handlers.polls.get_polls_summary_handler.GetPollsSummaryRequest")
    def test_execute(self, GetPollsSummaryRequest_mock):
        get_polls_summary_request_mock = Mock()
        GetPollsSummaryRequest_mock.return_value = get_polls_summary_request_mock

        request_mock = Mock()
        principal_mock = Mock()
        request_mock.principal = principal_mock

        expected_result_mock = Mock()
        self.use_case_mock.get_polls_summary.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        GetPollsSummaryRequest_mock.assert_called_once_with(principal_mock)
        self.use_case_mock.get_polls_summary.assert_called_once_with(
            get_polls_summary_request_mock
        )

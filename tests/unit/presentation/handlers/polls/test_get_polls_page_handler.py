from mock import Mock, patch

from presentation.handlers.polls import GetPollsPageHandler


class TestGetPollsPageHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter = None
        self.principal_util_mock = Mock()

        self.handler = GetPollsPageHandler(
            self.use_case_mock,
            self.presenter,
            self.principal_util_mock
        )

    @patch("presentation.handlers.polls.get_polls_page_handler.GetPollsPageRequest")
    def test_execute(self, GetPollsPageRequest_mock):
        get_polls_page_request_mock = Mock()
        GetPollsPageRequest_mock.return_value = get_polls_page_request_mock

        request_mock = Mock()
        principal_mock = Mock()
        request_mock.principal = principal_mock
        page = 1
        page_size = 10
        request_mock.args = {
            "page": page,
            "page_size": page_size
        }

        expected_result_mock = Mock()
        self.use_case_mock.get_polls_page.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        GetPollsPageRequest_mock.assert_called_once_with(
            principal_mock,
            None,
            page,
            page_size
        )
        self.use_case_mock.get_polls_page.assert_called_once_with(
            get_polls_page_request_mock
        )

from mock import Mock

from presentation.presenters import PagePresenter


class TestPagePresenter():
    def setup_method(self):
        self.item_presenter_mock = Mock()

        self.presenter = PagePresenter(self.item_presenter_mock)

    def test_init(self):
        assert self.presenter.item_presenter == self.item_presenter_mock

    def test_present(self):
        item_mock_1 = Mock()
        item_mock_2 = Mock()
        items_mock = [item_mock_1, item_mock_2]
        page_mock = Mock()
        page_mock.items = items_mock
        page_mock.page = 1
        page_mock.page_count = 3

        presented_mock = Mock()
        self.item_presenter_mock.present.return_value = presented_mock

        principal_mock = Mock()

        result = self.presenter.present(page_mock, principal_mock)

        assert result == {
            "items": [presented_mock, presented_mock],
            "page": page_mock.page,
            "page_count": page_mock.page_count
        }
        assert self.item_presenter_mock.present.call_count == 2
        self.item_presenter_mock.present.assert_any_call(
            item_mock_1,
            principal_mock
        )
        self.item_presenter_mock.present.assert_any_call(
            item_mock_2,
            principal_mock
        )

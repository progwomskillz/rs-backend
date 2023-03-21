from domain.entities.shared import Page


class TestPage():
    def setup_method(self):
        self.items = []
        self.page = 1
        self.page_count = 10

    def test_init(self):
        page = Page(self.items, self.page, self.page_count)

        assert page.items == self.items
        assert page.page == self.page
        assert page.page_count == self.page_count

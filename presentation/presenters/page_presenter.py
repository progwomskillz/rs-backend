class PagePresenter():
    def __init__(self, item_presenter):
        self.item_presenter = item_presenter

    def present(self, page, principal):
        return {
            "items": [
                self.item_presenter.present(item, principal)
                for item in page.items
            ],
            "page": page.page,
            "page_count": page.page_count
        }

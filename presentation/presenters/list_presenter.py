class ListPresenter():
    def __init__(self, item_presenter):
        self.item_presenter = item_presenter

    def present(self, items, principal):
        return [
            self.item_presenter.present(item, principal)
            for item in items
        ]

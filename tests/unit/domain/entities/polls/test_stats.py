from domain.entities.polls import Stats


class TestStats():
    def setup_method(self):
        self.title = "test_title"
        self.count = 25
        self.percentage = 50

        self.entity = Stats(self.title, self.count, self.percentage)

    def test_init(self):
        assert self.entity.title == self.title
        assert self.entity.count == self.count
        assert self.entity.percentage == self.percentage

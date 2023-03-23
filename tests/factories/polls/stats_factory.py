from domain.entities.polls import Stats


class StatsFactory():
    @staticmethod
    def generic():
        return Stats("family", 24, 50)

    @staticmethod
    def generate(title, count, percentage):
        return Stats(title, count, percentage)

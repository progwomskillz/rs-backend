from domain.entities.polls import Stats


class StatsTranslator():
    def from_document(self, document):
        return Stats(
            document.get("title"),
            document.get("count"),
            document.get("percentage")
        )

    def to_document(self, stats):
        return {
            "title": stats.title,
            "count": stats.count,
            "percentage": stats.percentage
        }

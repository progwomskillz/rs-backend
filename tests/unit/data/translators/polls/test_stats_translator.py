from data.translators.polls import StatsTranslator
from domain.entities.polls import Stats
from tests.factories.polls import StatsFactory


class TestStatsTranslator():
    def setup_method(self):
        self.translator = StatsTranslator()

    def test_from_document(self):
        document = {"title": "test_title", "count": 24, "percentage": 10}

        result = self.translator.from_document(document)

        assert isinstance(result, Stats) is True
        assert result.title == document["title"]
        assert result.count == document["count"]
        assert result.percentage == document["percentage"]

    def test_to_document(self):
        stats = StatsFactory.generic()

        result = self.translator.to_document(stats)

        assert result == {
            "title": stats.title,
            "count": stats.count,
            "percentage": stats.percentage
        }

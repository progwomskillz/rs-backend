class StatsPresenter():
    def present(self, stats, principal):
        return {
            "title": stats.title,
            "count": stats.count,
            "percentage": stats.percentage
        }

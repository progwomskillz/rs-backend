class Poll():
    def __init__(
            self, id, user, updated_at, community_name, community_size, feedbacks, summary
        ):
        feedbacks = feedbacks if feedbacks else []
        summary = summary if summary else []

        self.id = id
        self.user = user
        self.updated_at = updated_at
        self.community_name = community_name
        self.community_size = community_size
        self.feedbacks = feedbacks
        self.summary = summary

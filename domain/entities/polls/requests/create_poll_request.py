class CreatePollRequest():
    def __init__(self, principal, community_name, community_size, feedbacks):
        self.principal = principal
        self.community_name = community_name
        self.community_size = community_size
        self.feedbacks = feedbacks

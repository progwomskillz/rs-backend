class TokensPair():
    def __init__(self, access, refresh):
        self.access = access
        self.refresh = refresh

    def set_refresh(self, refresh):
        self.refresh = refresh

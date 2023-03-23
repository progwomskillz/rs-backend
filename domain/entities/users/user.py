class User():
    def __init__(self, id, role, username, password_hash, tokens_pairs, profile):
        tokens_pairs = tokens_pairs if tokens_pairs else []

        self.id = id
        self.role = role
        self.username = username
        self.password_hash = password_hash
        self.tokens_pairs = tokens_pairs
        self.profile = profile

    def on_create(self, id):
        self.id = id

    def on_login(self, tokens_pair):
        self.tokens_pairs.append(tokens_pair)

    def on_refresh(self, new_tokens_pair):
        self.tokens_pairs = [
            tokens_pair
            for tokens_pair in self.tokens_pairs
            if tokens_pair.refresh != new_tokens_pair.refresh
        ]
        self.tokens_pairs.append(new_tokens_pair)

    def on_logout(self, current_tokens_pair):
        self.tokens_pairs = [
            tokens_pair
            for tokens_pair in self.tokens_pairs
            if (
                tokens_pair.access != current_tokens_pair.access
                and tokens_pair.refresh != current_tokens_pair.refresh
            )
        ]

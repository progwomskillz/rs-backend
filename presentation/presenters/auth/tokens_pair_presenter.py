class TokensPairPresenter():
    def present(self, tokens_pair, principal):
        return {
            "access": tokens_pair.access,
            "refresh": tokens_pair.refresh
        }

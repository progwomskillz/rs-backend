import bcrypt


class BcryptWrapper():
    def __init__(self, complicity):
        self.complicity = complicity

    def compare(self, password, password_hash):
        return bcrypt.checkpw(password.encode(), password_hash)

    def hash(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(self.complicity))

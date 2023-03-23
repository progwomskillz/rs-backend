class CreateUserRequest():
    def __init__(self, principal, role, username, password, first_name, last_name):
        self.principal = principal
        self.role = role
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

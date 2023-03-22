class GetUsersPageRequest():
    def __init__(self, principal, role, page, page_size):
        self.principal = principal
        self.role = role
        self.page = page
        self.page_size = page_size

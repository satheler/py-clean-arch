class Account(object):
    id: str
    email: str
    password: str

    def __eq__(self, to_compare) -> bool:
        if (isinstance(to_compare, Account)):
            return self.id == to_compare.id \
                and self.email == to_compare.email \
                and self.password == to_compare.password

        return False

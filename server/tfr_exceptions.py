class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class IDLoginError(MyError):
    pass

class PasswordLoginError(MyError):
    pass

class UserInputError(MyError):
    pass

class InteractionLoginError(MyError):
    pass

class ContactInfoIDError(MyError):
    pass

class FinancialUpdateIDError(MyError):
    pass

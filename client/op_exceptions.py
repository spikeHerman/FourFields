class MyError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class IDError(MyError):
    pass
    
class PWDError(MyError):
    pass

class NoChangesError(MyError):
    pass

class ProgramError(MyError):
    pass

class SupporterIDError(MyError):
    pass

class EntryLength(MyError):
    def __init__(self, entry):
        self.entry = entry

class CommentLength(MyError):
    def __init__(self, comment):
        self.comment = comment

class NoChangesError(MyError):
    pass

class NoMoreSupportersError(MyError):
    pass

class NoPreviousSupporter(MyError):
    pass

class IsBeingCalledError(MyError):
    pass

class WrongDeviceError(MyError):
    pass

class ScheduledCallError(MyError):
    pass

from exception.base import BombShellException


class CoreException(BombShellException):
    pass


class RecoverableException(CoreException):
    pass


class UnrecoverableException(CoreException):
    pass


class PrerequisiteException(UnrecoverableException):
    pass


class ExtractException(RecoverableException):
    def __init__(self, partial_data: dict, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.partial = partial_data

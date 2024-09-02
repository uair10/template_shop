from dataclasses import dataclass


class AppException(Exception):
    """Base Exception"""

    @property
    def message(self) -> str:
        return "An application error occurred"


class ApplicationException(AppException):
    pass


class UnexpectedError(ApplicationException):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass


class MappingError(ApplicationException):
    pass


@dataclass
class BaseTgException(ApplicationException):
    msg_for_user: str | None

    def __repr__(self) -> str:
        result_msg = f"Error: {self.message}"
        if self.msg_for_user:
            result_msg += f". Information for user: {self.msg_for_user}"

        return result_msg

    def __str__(self) -> str:
        return f"{self.__class__.__name__}\n" f"text: {self.message}\n" f"notify info: {self.msg_for_user}"

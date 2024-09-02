from dataclasses import dataclass

from .common import BaseTgException


@dataclass
class UserIdNotExist(BaseTgException):
    msg_for_user: str = "user-not-exists-msg"


@dataclass
class UserTgIdNotExist(BaseTgException):
    msg_for_user: str = "user-not-exists-msg"


@dataclass
class UserIdAlreadyExist(BaseTgException):
    msg_for_user: str = "user-already-exists-msg"

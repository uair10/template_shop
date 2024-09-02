from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from template_shop.core.exceptions.user import UserIdNotExist, UserTgIdNotExist
from template_shop.infrastructure.database.exception_mapper import exception_mapper
from template_shop.infrastructure.database.models import User
from template_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class UserRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_user_by_id(self, user_id: int) -> User:
        """Получаем пользователя по id"""

        user: User | None = await self._session.scalar(
            select(User)
            .where(
                User.id == user_id,
            )
            .with_for_update(),
        )
        if not user:
            raise UserIdNotExist

        return user

    @exception_mapper
    async def get_user_by_tg_id(self, user_tg_id: int, joined: bool = False) -> User:
        """Получаем пользователя по telegram id"""

        query = select(User).where(
            User.telegram_id == user_tg_id,
        )
        if joined:
            query = query.options(joinedload(User.promocodes))

        user: User | None = await self._session.scalar(query)

        if not user:
            raise UserTgIdNotExist

        return user

    @exception_mapper
    async def create_user(self, user: User) -> None:
        """Создаем пользователя"""

        self._session.add(user)
        try:
            await self._session.flush((user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def update_user(self, user: User) -> None:
        """Обновляем пользователя"""

        try:
            await self._session.merge(user)
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def get_users(self) -> list[User]:
        """Получаем пользователей"""

        res = await self._session.scalars(select(User))
        users: list[User] = list(res)

        return users

    @staticmethod
    def _parse_error(err: DBAPIError, user: User) -> None:
        """Определение ошибки"""

        ...

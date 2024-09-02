from template_shop.core.models.enums.user import LangCode
from template_shop.infrastructure.database.models import User
from template_shop.infrastructure.database.uow import SQLAlchemyUoW


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, uow: SQLAlchemyUoW) -> None:
        self._uow = uow

    async def get_user_by_id(self, user_id: int) -> User:
        """Получаем пользователя по id"""

        return await self._uow.user_repo.get_user_by_id(user_id)

    async def get_user_by_telegram_id(self, user_tg_id: int) -> User:
        """Получаем пользователя по telegram id"""

        return await self._uow.user_repo.get_user_by_tg_id(user_tg_id)

    async def increase_user_balance(self, user_tg_id: int, amount: float) -> None:
        """Увеличиваем баланс пользователя"""

        user = await self._uow.user_repo.get_user_by_tg_id(user_tg_id)
        user.balance += amount

        await self._uow.user_repo.update_user(user=user)

        await self._uow.commit()

    async def add_promocode_to_user(self, user_tg_id: int, promocode_id: int) -> None:
        """Добавляем промокод юзеру"""

        user = await self._uow.user_repo.get_user_by_tg_id(user_tg_id, joined=True)
        promocode = await self._uow.promocode_repo.get_promocode_by_id(promocode_id)
        user.promocodes.append(promocode)

        await self._uow.user_repo.update_user(user=user)

        await self._uow.commit()

    async def change_user_lang(self, user_tg_id: int, lang_code: LangCode) -> None:
        """Изменяем язык пользователя"""

        user: User = await self._uow.user_repo.get_user_by_tg_id(user_tg_id)
        user.lang_code = lang_code

        await self._uow.user_repo.update_user(user)

        await self._uow.commit()

    async def create_user(self, telegram_id: int, username: str) -> None:
        """Создаем пользователя"""

        user = User(telegram_id=telegram_id, username=username)
        try:
            await self._uow.user_repo.create_user(user)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()

    async def get_all_users(self) -> list[User]:
        """Получаем всех пользователей"""

        return await self._uow.user_repo.get_users()

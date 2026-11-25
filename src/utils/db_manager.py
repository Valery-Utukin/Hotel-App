from src.repositories.users import UserRepository
from src.repositories.hotels import HotelRepository
from src.repositories.rooms import RoomRepository
from src.repositories.bookings import BookingRepository


# Класс который хэндлит (ну или будет хэндлить) всю работу с БД на уровне бизнес-логики.
class DBManager:
    """
    Представляет собой самописный контекстный менеджер (async with). При инициализации (__init__)
    ему в качестве параметра передается это -> sqlalchemy.ext.asyncio.session.async_sessionmaker
    и "обзывается" фабрикой сессий. При каждом запуске такого контекстного менеджера (__aenter__),
    эта фабрика сессий вызывается и создает сессию для данного экземпляра DBManager'а.
    При работе с БД, для фиксации изменений нужно использовать метод commit(). Опять же,
    если я правильно понял: в случае выполнения логики в этом контекстном менеджере, если выполнение
    прервется (ошибка выполнения), то изменения которые яв-ся неконсистентными (ACID)
    нужно откатить назад. Для этого при закрытии менеджера (__aexit__) сначала делается rollback,
    а уже потом закрывается соединение с БД. Все изменения, которые нам нужны,
    мы коммитим сами (self.commit).
    """
    def __init__(self, session_factory):
        # Пока просто создаем атрибут фабрики
        self.session_factory = session_factory

    async def __aenter__(self):
        """
        Выполняется при входе в контекст (после async with)
        :return: Экземпляр DBManager
        """
        # Вызываем фабрику, чтобы получить сессию
        self.session = self.session_factory()

        # Создаем атрибуты репозиториев, через которые выполняются запросы к БД
        self.users = UserRepository(self.session)
        self.hotels = HotelRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.bookings = BookingRepository(self.session)

        # Возвращаем готовый к работе экземпляр
        return self

    async def __aexit__(self, *args):
        """
        Выполняется при выходе из контекста
        :param args: Не помню какие это конкретно аргументы, пока не используются
        :return: Ничего
        """
        # Сначала откатываем все несохраненные изменения в БД (rollback)
        # и потом закрываем соединение с базой (close)
        try:
            await self.session.rollback()
        finally:
            await self.session.close()

    async def commit(self):
        """
        Сохраняем изменения в БД
        :return: Ничего
        """
        await self.session.commit()
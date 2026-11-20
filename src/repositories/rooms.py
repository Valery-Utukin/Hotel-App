from sqlalchemy import select, insert, delete

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room


class RoomRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_all(
            self,
            hotel_id,
            title,
            min_price,
            max_price,
            min_quantity,
            max_quantity,
            limit,
            offset,
    ):
        # Основной запрос на выборку по конкретному отелю (hotel_id)
        query = select(self.model).where(self.model.hotel_id == hotel_id)

        # Фильтрация по названию (если есть)
        if title:
            query = query.where(self.model.title.ilike(f"%{title}%"))

        # Фильтрация по мин. и макс. цене (если есть)
        if min_price and max_price:
            query = query.where(self.model.price.between(min_price, max_price))
        elif min_price and not max_price:
            query = query.where(self.model.price.__ge__(min_price))
        elif max_price and not min_price:
            query = query.where(self.model.price.__le__(max_price))

        # Фильтрация по мин. и макс. кол-ву таких номеров (если есть)
        if min_quantity and max_quantity:
            query = query.where(self.model.quantity.between(min_quantity, max_quantity))
        elif min_quantity and not max_quantity:
            query = query.where(self.model.quantity.__ge__(min_quantity))
        elif max_quantity and not min_quantity:
            query = query.where(self.model.quantity.__le__(max_quantity))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
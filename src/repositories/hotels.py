from sqlalchemy import select, insert, delete

from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.models.hotels import HotelsORM


class HotelRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel


    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsORM)
        if title:
            query = query.where(HotelsORM.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsORM.location.ilike(f"%{location}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

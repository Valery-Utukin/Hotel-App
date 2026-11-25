from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, limit: int = 10, offset: int = 0, **filter_by):
        query = select(self.model).filter_by(**filter_by).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, limit: int = 10, offset: int = 0, **kwargs):
        return await self.get_filtered(limit=limit, offset=offset, **kwargs)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)


    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)


    async def update(self, data: BaseModel, is_patch: bool = False, **filter_by):
        """

        :param data:
        :param is_patch: Важная штука, которая подвязывается к параметру Pydantic (exclude_unset).
        Благодаря ей можно использовать базовый метод update как для ручки PUT, так и для PATCH.
        В случае PUT, этот параметр должен быть установлен как False (Просто не указываем его,
        т.к. по дефолту - False). В случае PATCH, устанавливаем его в True и тогда все значения,
        которые не были указаны, будут исключены из запроса к БД. Как раз поведение метода PATCH.
        :param filter_by: Фильтры для обновления. Например, можно обновить по-конкретному id,
        или по значениям столбцов.
        :return:
        """
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=is_patch))
            .filter_by(**filter_by)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)

        return result.scalars().one()


    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

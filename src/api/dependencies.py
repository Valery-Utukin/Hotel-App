from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1, description="Номер страницы с Отелями")]
    per_page: Annotated[int, Query(3, ge=1, lt=10, description="Кол-во Отелей на страницу")]


PaginationDep = Annotated[PaginationParams, Depends()]

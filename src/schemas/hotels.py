from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    cost: int


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    cost: int | None = Field(None)
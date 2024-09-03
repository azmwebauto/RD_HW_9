import re
from datetime import datetime

from pydantic import BaseModel
from pydantic import field_serializer, Field, field_validator

from app import config


class TimeSchema(BaseModel):
    published_date: datetime
    last_modified_date: datetime

    @field_serializer('published_date')
    def serialize_published_date(self, value: datetime) -> datetime:
        return value.replace(tzinfo=None)

    @field_serializer('last_modified_date')
    def serialize_last_modified_date(self, value: datetime) -> datetime:
        return value.replace(tzinfo=None)


class PostCve(TimeSchema):
    cve_id: str
    description: str | None = None
    title: str | None = None
    problem_types: str | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    'cve_id': 'CVE-1234-1234',
                    'description': 'Description',
                    'title': 'Title',
                    'problem_types': 'TypeOne, TypeTwo, TypeThree',
                    'published_date': '2024-08-28T09:50:36.321Z',
                    'last_modified_date': '2024-08-28T09:50:36.321Z'
                }
            ]
        }

    @field_validator('cve_id')
    def cve_is_valid(cls, cve_id):
        pattern = re.compile(r'CVE-.?')
        if not pattern.search(cve_id):
            raise ValueError(f'{cve_id=} is not matching pattern {pattern}')
        return cve_id


class ReadCve(PostCve):
    id: int
    description: str
    title: str
    problem_types: str


class PostManyCves(BaseModel):
    data: list[PostCve] = Field(max_items=config.MAX_CVE_ITEMS)


class DeleteResult(BaseModel):
    result: int


class PostCveSuccess(BaseModel):
    message: str
    amount_added: int


class UpdateCve(TimeSchema):
    description: str | None = None
    title: str | None = None
    problem_types: str | None = None
    published_date: datetime = None
    last_modified_date: datetime = None

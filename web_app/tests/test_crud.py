import datetime

import pytest
import sqlalchemy
from pydantic_core._pydantic_core import ValidationError

from app.cves import crud, schemas


@pytest.mark.asyncio
class TestCveRepo:

    @pytest.mark.order(1)
    async def test_create(self, session):
        cve = schemas.PostCve(cve_id='CVE-1234-1234',
                              description='test',
                              title='test',
                              problem_types='CWE-78', published_date=datetime.datetime(2017, 11, 2, 16, 0),
                              last_modified_date=datetime.datetime(2024, 8, 5, 18, 28, 16, 743000))
        db_res = await crud.CveRepository.create_many(session, [cve.model_dump()])
        print(db_res)
        assert len(db_res) > 0

    @pytest.mark.order(2)
    async def test_get_many(self, session):
        await self.test_create(session)
        cves = await crud.CveRepository.get_many(session, limit=1)
        print(cves)
        assert cves != []

    @pytest.mark.order(3)
    async def test_get_one_by_cve_id(self, session):
        await self.test_create(session)
        test_id = 'CVE-1234-1234'
        cve = await crud.CveRepository.get_one_by_cve_id(session, test_id)
        print(cve)
        assert cve is not None

    @pytest.mark.order(4)
    async def test_get_one_by_id(self, session):
        await self.test_create(session)
        test_id = 1
        cve = await crud.CveRepository.get_one_by_id(session, test_id)
        print(cve)
        assert cve is not None

    @pytest.mark.order(5)
    async def test_delete_one_by_id(self, session):
        await self.test_create(session)
        test_id = 1
        cve = await crud.CveRepository.delete_one_by_id(session, test_id)
        print(cve)
        assert cve is not None

    @pytest.mark.order(6)
    async def test_failed_create(self, session):
        cve = dict(description='test',
                   title='test',
                   problem_types='CWE-78', published_date=datetime.datetime(2017, 11, 2, 16, 0),
                   last_modified_date=datetime.datetime(2024, 8, 5, 18, 28, 16, 743000))
        try:
            db_res = await crud.CveRepository.create_many(session, [cve])
            print(db_res)
        except sqlalchemy.exc.IntegrityError as e:
            assert type(e) is sqlalchemy.exc.IntegrityError

    async def test_schema(self):
        cve = dict(description='test', cve_id='CVE', raw_info={},
                   title='test',
                   problem_types='CVE-78', published_date=datetime.datetime(2017, 11, 2, 16, 0),
                   last_modified_date=datetime.datetime(2024, 8, 5, 18, 28, 16, 743000))
        try:
            schema = schemas.PostCve(**cve)
        except ValidationError as e:
            assert type(e) is ValidationError

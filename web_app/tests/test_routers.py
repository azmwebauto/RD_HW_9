import pytest
from pydantic_core._pydantic_core import ValidationError

from app.cves import schemas
from app.cves.router import get_one_by_id, get_all, create_cves, delete_one_by_id, get_one_by_cve_id
from app.main import get_status


@pytest.mark.asyncio
class TestCveRouter:
    @pytest.mark.asyncio
    async def test_get_status(self):
        response = await get_status()
        print(response)
        assert response.body.decode() == 'OK'

    @pytest.mark.order(1)
    async def test_create_one(self, session):
        cves = {
            "data": [
                {
                    "raw_info": {},
                    "cve_id": "CVE-1234-1234",
                    "description": "test",
                    "title": "test",
                    "problem_types": "test",
                    "published_date": "2024-08-27T13:54:36.007Z",
                    "last_modified_date": "2024-08-27T13:54:36.007Z"
                }
            ]
        }

        result = await create_cves(db_session=session, cves=schemas.PostManyCves(**cves))
        print(result)
        assert result is not None

    @pytest.mark.order(2)
    async def test_get_many(self, session):
        await self.test_create_one(session)
        result = await get_all(db_session=session)
        print(result)
        assert result != []

    @pytest.mark.order(3)
    async def test_router_get_cve_by_id(self, session):
        await self.test_create_one(session)
        test_id = 1
        result = await get_one_by_id(db_session=session, id_=test_id)
        print(result)
        assert result is not None

    @pytest.mark.order(4)
    async def test_router_get_cve_by_cve_id(self, session):
        await self.test_create_one(session)
        test_id = 'CVE-1234-1234'
        result = await get_one_by_cve_id(db_session=session, cve_id=test_id)
        print(result)
        assert result is not None

    @pytest.mark.order(5)
    async def test_delete_one(self, session):
        await self.test_create_one(session)
        test_id = 1
        result = await delete_one_by_id(db_session=session, id_=test_id)
        print(result)
        result = await get_all(db_session=session)
        print(result)
        assert result.data == []

    @pytest.mark.order(6)
    async def test_failed_create_one(self, session):
        cves = {
            "cves": [
                {
                    "raw_info": {},
                    "cve_id": "",
                    "description": "",
                    "title": "",
                    "problem_types": "",
                    "published_date": "2024-08-27T13:54:36.007Z",
                    "last_modified_date": "2024-08-27T13:54:36.007Z"
                }
            ]
        }
        try:
            many_cves = schemas.PostManyCves(**cves)
            result = await create_cves(db_session=session, cves=many_cves)
            print(result.data)
        except ValidationError as e:
            assert type(e) is ValidationError
        cves = {
            "cves": [
                {
                    "raw_info": {},
                    "cve_id": "12361-EGWEHWWJ",
                    "description": "",
                    "title": "",
                    "problem_types": "",
                    "published_date": "2024-08-27T13:54:36.007Z",
                    "last_modified_date": "2024-08-27T13:54:36.007Z"
                },
            ]
        }
        try:
            result = await create_cves(db_session=session, cves=schemas.PostManyCves(**cves))
            print(result)
        except ValidationError as e:
            assert type(e) is ValidationError
        cves = {
            "cves": [
                {
                    "raw_info": {},
                    "cve_id": f"CVE-1231-{i}",
                    "description": "",
                    "title": "",
                    "problem_types": "",
                    "published_date": "2024-08-27T13:54:36.007Z",
                    "last_modified_date": "2024-08-27T13:54:36.007Z"
                } for i in range(1001)
            ]
        }
        try:
            result = await create_cves(db_session=session, cves=schemas.PostManyCves(**cves))
        except ValidationError as e:
            assert type(e) is ValidationError
        result = await get_all(db_session=session)
        assert result.data == []

    async def test_create_many(self, session):
        cves = {
            "data": [
                {
                    "raw_info": {},
                    "cve_id": f"CVE-1231-{i}",
                    "description": "",
                    "title": "",
                    "problem_types": "",
                    "published_date": "2024-08-27T13:54:36.007Z",
                    "last_modified_date": "2024-08-27T13:54:36.007Z"
                } for i in range(100)
            ]
        }
        result = await create_cves(db_session=session, cves=schemas.PostManyCves(**cves))
        print(result)
        result = await get_all(db_session=session)
        assert len(result.data) == 100

    async def test_failed_create_many(self, session):
        cves = {
            "data": [
                {
                    "raw_info": {},
                    "cve_id": f"CVE-1231-{i}",
                    "description": "",
                    "title": "",
                    "problem_types": "",
                    "published_date": "2024-08-27T13:54:36.007Z",
                    "last_modified_date": "2024-08-27T13:54:36.007Z"
                } for i in range(1000)
            ]
        }
        result = await create_cves(db_session=session, cves=schemas.PostManyCves(**cves))
        print(result)
        result = await get_all(db_session=session, limit=10_000)
        assert len(result.data) == 1000

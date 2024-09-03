import logging
from typing import Mapping, Sequence

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.cves import models


class CveRepository:
    @staticmethod
    async def delete_one_by_id(session: AsyncSession, id_: int):
        statement = delete(models.CveModel).where(models.CveModel.id == id_).returning(models.CveModel.id)
        try:
            cursor_result = await session.execute(statement)
            await session.commit()
            return cursor_result.scalars().first()
        except Exception as e:
            logging.error(e)
            await session.rollback()

    @staticmethod
    async def get_one_by_id(session: AsyncSession, id_: int) -> models.CveModel | None:
        statement = select(models.CveModel).where(models.CveModel.id == id_)
        cve_instance = await session.execute(statement)
        return cve_instance.scalar_one_or_none()

    @staticmethod
    async def get_one_by_cve_id(session: AsyncSession, cve_id: str) -> models.CveModel | None:
        statement = select(models.CveModel).where(models.CveModel.cve_id == cve_id)
        cve_instance = await session.execute(statement)
        result = cve_instance.scalar_one_or_none()
        return result

    @staticmethod
    async def create_many(session: AsyncSession, cves: Sequence[Mapping]) -> Sequence[models.CveModel]:
        stmt = insert(models.CveModel).returning(models.CveModel).values(cves)
        result = await session.execute(stmt)
        results = result.scalars().all()
        await session.commit()
        return results

    @staticmethod
    async def get_many(session: AsyncSession, limit: int = 100, offset: int = 0) -> Sequence[models.CveModel]:
        statement = select(models.CveModel).limit(limit).offset(offset)
        res = await session.execute(statement)
        return res.scalars().all()

    @staticmethod
    async def update_one_by_cve_id(session: AsyncSession, cve_id: str, data: Mapping) -> models.CveModel | None:
        statement = update(models.CveModel).where(models.CveModel.cve_id == cve_id).returning(models.CveModel)
        res = await session.execute(statement, data)
        await session.commit()
        return res.scalars().first()

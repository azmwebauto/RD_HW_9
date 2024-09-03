import logging
from typing import Annotated, Sequence

import sqlalchemy
from fastapi import APIRouter, Path, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.cves import crud, models, schemas
from app.deps import get_db

router = APIRouter(prefix="/cves")


@router.get("/id/{id}")
async def get_one_by_id(
        id_: int = Path(..., title="The ID of the CVE", gt=0, alias='id'),
        db_session: AsyncSession = Depends(get_db)
) -> schemas.ReadCve:
    result = await crud.CveRepository.get_one_by_id(db_session, id_)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return schemas.ReadCve.model_validate(result)


@router.get("/cve_id/{cve_id}")
async def get_one_by_cve_id(
        cve_id: str = Path(..., title="The ID of the CVE", alias='cve_id'),
        db_session: AsyncSession = Depends(get_db)
) -> schemas.ReadCve:
    result = await crud.CveRepository.get_one_by_cve_id(db_session, cve_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return schemas.ReadCve.model_validate(result)


@router.delete("/{id}")
async def delete_one_by_id(
        id_: int = Path(..., title="The ID of the CVE", gt=0, alias='id'),
        db_session: AsyncSession = Depends(get_db)
):
    result = await crud.CveRepository.delete_one_by_id(db_session, id_)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {'result': result}


@router.get("/")
async def get_all(
        limit: Annotated[int, Query(gt=0, le=1_000)] = 100,
        offset: Annotated[int, Query(ge=0)] = 0,
        db_session: AsyncSession = Depends(get_db)
) -> list[schemas.ReadCve]:
    result = await crud.CveRepository.get_many(db_session, limit, offset)
    return [schemas.ReadCve.model_validate(i) for i in result]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_cves(cves: schemas.PostManyCves, db_session: AsyncSession = Depends(get_db)) -> schemas.PostCveSuccess:
    try:
        cves_: Sequence[models.CveModel] = await crud.CveRepository.create_many(
            db_session, [i.model_dump() for i in cves.data]
        )
        return schemas.PostCveSuccess(message='CVEs created', amount_added=len(cves_))
    except sqlalchemy.exc.IntegrityError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='CVE already exists')
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from database import get_db
from model.models import GDPRecord # orm modeli
from schemas.ingestion import  GDPRecordResponse # Pydantic Yanıt Şeması

router=APIRouter(prefix="/gdp",tags=["GDP Verileri"])

@router.get("/records",response_model=list[GDPRecordResponse])
async def list_gdp_records(
    country_code: str | None = Query(None, description="Ülke kodu süzgeci (ör. TUR)"),
    year: int | None = Query(None, description="Yıl süzgeci (ör. 2020)"),
    limit: int = Query(50, ge=1, le=200, description="Getirilecek maksimum satır sayısı"),
    offset: int = Query(0, ge=0, description="Atlanacak satır sayısı (Sayfalama)"),
    db: AsyncSession = Depends(get_db)
):
    # Select sorgusu
    stmt=select(GDPRecord).order_by(GDPRecord.id)

    # Dinamik filtreler
    if country_code:
        stmt=stmt.where(GDPRecord.country_code==country_code.upper())
    if year:
        stmt=stmt.where(GDPRecord.year==year)

    stmt=stmt.offset(offset).limit(limit)

    result=await db.scalars(stmt)
    records=result.all()

    return records

@router.get("/records/{record_id}",response_model=GDPRecordResponse)
async def get_gdp_record_detail(record_id:int,db:AsyncSession=Depends(get_db)):

    stmt=select(GDPRecord).where(GDPRecord.id==record_id)
    result=await db.scalars(stmt)
    record=result.first()

    if not record:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID={record_id} olan kayıt bulunamadı."
        )

    return record


from fastapi import APIRouter,HTTPException,status,Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from model import models
from schemas import ingestion
from services import ingetion_service


router=APIRouter(prefix="/ingestion",tags=["Ingestion"])

@router.post("/process-csv",
 response_model=ingestion.IngestionResponse,
 status_code=status.HTTP_201_CREATED
)
async def process_csv_endpoint(
    url:str=Query(
        "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv",
        description="İndirilecek CSV dosyasının direkt URL adresi"
    ),
    db:AsyncSession=Depends(get_db)
):
    try:
        inserted_count=await ingetion_service.IngestionService.ingest_csv_data(db=db,url=url)

        return ingestion.IngestionResponse(
            status="success",
            message="CSV verisi başarıyla indirildi ve veritabanına kaydedildi.",
            inserted_records=inserted_count
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Veri yükleme işlemi sırasında hata oluştu: {str(e)}"
        )


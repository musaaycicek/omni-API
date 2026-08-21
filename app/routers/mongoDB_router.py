from fastapi import APIRouter,HTTPException,status,Query
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.mongoDB_schemas as mongoSchemas
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from services import ingetion_service


router=APIRouter(prefix="/mongoGET",tags=["Mongo GET"])

# Mongo db içerisinden verileri al
@router.get(
    "/mongoDB_GET",
    response_model=list[mongoSchemas.mongoResponse], # Dönüş tipini liste yaptık
    status_code=status.HTTP_200_OK
)

async def mongoDB_GET(
   colection_namestr:str = Query("gdp_records", description="Çekilecek MongoDB koleksiyon adı")):
    try:
     getDB=await ingetion_service.IngestionService._get_all_mongoDB(colection_namestr)
     return getDB

    except PyMongoError as e:
        print(f"MongoDB Hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MongoDB verileri çekilirken bir veritabanı hatası oluştu."
        )
    except Exception as e:
        print(f"Beklenmeyen Hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bir hata oluştu: {str(e)}"
        )





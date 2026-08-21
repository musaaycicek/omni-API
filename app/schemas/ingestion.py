from pydantic import BaseModel,ConfigDict


# 1. POST /process-csv endpoint'i çalıştığında dönecek yanıt şeması
class IngestionResponse(BaseModel):
    status:str
    message:str
    inserted_records:int


# 2. GET /records endpoint'i çalıştığında veritabanından dönen satırları temsil edecek şema
class GDPRecordResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # Hem '_id' hem 'id' kullanımını destekler
    ) # ORM nesnesini Pydantic'e dönüştürmek için şart!

    id: int
    country_name: str
    country_code: str
    year: int
    value: float | None
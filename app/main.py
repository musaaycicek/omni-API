from fastapi import FastAPI

# Router dosyalarından APIRouter nesnelerini import ediyoruz
from routers.ingestion_router import router as ingestion_router
from routers.gdp_router import router as gdp_router
from routers.mongoDB_router import router as mongo_router  # Yeni eklediğimiz MongoDB router'ı

app = FastAPI(  
    title="Omni API",
    description="Omni API,transform data 3 format",
    version="1.0.0"
)

# Router'ları uygulamaya dahil ediyoruz
app.include_router(ingestion_router, prefix="/api/csv")
app.include_router(gdp_router, prefix="/api/gdp")
app.include_router(mongo_router, prefix="/api/mongo")  # MongoDB rotasını bağlıyoruz

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Harcama ve Gelir Takip API'sine Hoş Geldin Musa!"}
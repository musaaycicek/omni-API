
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.orm import DeclarativeBase

# 1. Asenkron SQLite Bağlantı Cümlesi (sqlite+aiosqlite kullanılıyor)
DATABASE_URL = "sqlite+aiosqlite:///./datashift.db"

#async engine oluşturma
# echo=True gelişim aşamasında çalıştırılırken sql komutlarını gösterir

engine=create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread":False} # SQLite özelindeki  thread kilidini  kaldırır
)

AsyncSessionLocal=async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # Commit sonrası nesnelerin oturumdan düşmesini engeller
    autoflush=False
)

class Base(DeclarativeBase):
    pass


async def init_db():
   async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all(bind=engine))

# FastAPI Dependency (Her isteğe özel asekron DB oturumu açıp kapatır)
async def get_db()->AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
       try: 
         
         yield session

       except Exception as e:
          print(f"{e}")

       finally:
          session.close()




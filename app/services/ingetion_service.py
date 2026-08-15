
import httpx
import io
import os
from pathlib import Path
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from model.models import GDPRecord

mongo_uri: str = "mongodb://localhost:27017"
db_name: str = "mongoDB_omniAPI"

class IngestionService():

   @staticmethod
   async def _download_csv_from_url(url="https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"):
      kayit_yeri=Path("./data/csv_get.csv")

      buffer=io.BytesIO()

      if not os.path.exists(kayit_yeri):
         kayit_yeri.parent.mkdir(parents=True,exist_ok=True)

         async with httpx.AsyncClient() as client:
         
         #istek atma durumu(state)
          async with client.stream("GET",url=url) as response:
            response.raise_for_status() # HTTP 404/500 kontrolü
           
            with open(kayit_yeri,"wb") as dosya:
               # response.aiter_bytes(8132) : Gelen veriyi 8 kb (chunk = parçalar) olarak çeker
               # aiter_bytes = byte_iterator bu yüzden döngüye kullandık
               async for chunk in response.aiter_bytes(chunk_size=8192):
                  dosya.write(chunk) # csv dosyamıza local de kaydeder
                  buffer.write(chunk) # buffer olarak kaydeder
      else:
         # dosya varsa buffer'a yükle("rb" ile oku) 
         with open(kayit_yeri,"rb") as dosya:
            buffer.write(dosya.read())

      
      # Okuma işleminde imleci en başa çeker
      buffer.seek(0)

      return buffer
    
   @staticmethod    
   async def _process_and_save_csv(file_bytes:io.BytesIO,db:AsyncSession)->int:
      # Dosyamızı(csv) okuma  işlemi yapıyoruz. download_csv_from_url ile çekilen csv dosyamızı
      # düzenledikten sonra csv den dict çeviriyoruz nedeni ise  model içine elemanları yazmamız lazım 
      # dataframe'i to_dict(orient=(dataframe neye göre düzenleme yapıcaz)) orient="records" her bir sütun için key oluşturur
      # 
      #   {"country_code": "TUR", "year": 2020, "value": 720000},
      #   {"country_code": "USA", "year": 2020, "value": 2100000}


      # Pandas ile bellekteki CSV'yi okuma
      df=pd.read_csv(file_bytes)


      df=df.rename(columns={
        "Country Name": "country_name",
        "Country Code": "country_code",
        "Year": "year",
        "Value": "value"
      })

      df["value"]=df["value"].fillna(0.0)

      records=df.to_dict(orient="records")

     
      # 5. Dict listesini SQLAlchemy ORM nesnelerine dönüştür
      
      db_objects = [
            GDPRecord(
                country_name=row["country_name"],
                country_code=row["country_code"],
                year=int(row["year"]),
                value=float(row["value"])
            )
            for row in records
        ]

      db.add_all(db_objects)
      await db.commit()

      #
      return records

   @staticmethod
   async def _insert_mongoDB(veriler:list[dict],col_name:str):

      try:
         # Dinamik olması için [] içinde yazdık


         # ilk önce istemci oluşturulur
         client=MongoClient(mongo_uri)
         

         # DB oluşturulur
         db=client[db_name]

         # Koleksiyon oluşturma
         koleksiyon=db[col_name]

         # Verileri döngü ile al ve koleksiyona kaydet
         for veri in veriler:

            koleksiyon.update_many(
               {"country_code":veri["country_code"]},
               {"$set",veri},upsert=True
            )
         client.close()


      except PyMongoError as e:
         print(f"{e}")


      


   @staticmethod
   async def ingest_csv_data(db:AsyncSession,url:str)->int:

      buffer=await IngestionService._download_csv_from_url(url)

      saved_count=await IngestionService._process_and_save_csv(buffer,db)

      mongo_ins= await IngestionService._insert_mongoDB(saved_count)

      return mongo_ins


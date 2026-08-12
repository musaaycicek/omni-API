
import httpx
import io
import os
from pathlib import Path
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from model.models import GDPRecord

class IngestionService():

   @staticmethod
   async def _download_csv_from_url(url="https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"):
      kayit_yeri=Path("./data/csv_get.csv")

      buffer=io.BytesIO()

      if not os.path.exists(kayit_yeri):
         kayit_yeri.parent.mkdir(parents=True,exist_ok=True)
      else:
         # dosya varsa buffer a yükle("rb" ile oku) 
         with open(kayit_yeri,"rb") as dosya:
            buffer.write(dosya.read())

      

      async with httpx.AsyncClient() as client:
        
        #istek atma durumu(state)
        async with client.stream("GET",url=url) as response:
         # response.aiter_bytes(8132) : Gelen veriyi 8 kb (chunk = parçalar) olarak çeker
         with open(kayit_yeri,"wb") as dosya:
            # aiter_bytes = byte_iterator bu yüzden dönhü kullandık
            async for chunk in response.aiter_bytes(chunk_size=8192):
               dosya.write(chunk) # csv dosyamıza local de kaydeder
               buffer.write(chunk) # buffer olarak kaydeder

      # Okuma işleminde imleci en başa çeker
      buffer.seek(0)

      return buffer
    
   @staticmethod    
   async def _process_and_save_csv(file_bytes:io.BytesIO,db:AsyncSession)->int:
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

      db_object=[
         GDPRecord(
            
         )
      ]


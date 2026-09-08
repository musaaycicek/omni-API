
from pydantic import BaseModel,ConfigDict



"""
        _id (MongoDB otomatik atar, Pydantic'te id olarak eşlenecek)

        country_name (Metin / String)

        country_code (Metin / String - ör. "TUR")

        year (Tam Sayı / Integer)

        value (Odalı Sayı / Float veya Null)    """


class mongoBase(BaseModel):

       country_name:str
       year:int
       value:float


class mongoCraete(BaseModel):pass


class mongoResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # Hem '_id' hem 'id' kullanımını destekler
    )
    _id:int
    country_code:str

  





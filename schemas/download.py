from pydantic import BaseModel

# Modelo Pydantic para los datos de entrada
class DownloadCreate(BaseModel):
    user_id: int
    filename: str

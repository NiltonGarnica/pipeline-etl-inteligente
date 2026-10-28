from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Pipeline ETL Inteligente"}


@app.get("/health")
def verificar_salud():
    return {
        "status": "ok",
        "service": "pipeline-etl-inteligente"
    }

from pydantic import BaseModel

class TextoEntrada(BaseModel):
    texto: str

@app.post("/process")
def procesar_texto(datos: TextoEntrada):
    return {
        "texto_original": datos.texto,
        "mensaje": "Texto recibido correctamente"
    }
class TextoEntrada(BaseModel):
    texto: str
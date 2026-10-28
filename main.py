
from fastapi import FastAPI, HTTPException
from requests import RequestException

from schemas import TextoEntrada
from llm_service import analizar_texto

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


@app.post("/process")
def procesar_texto(datos: TextoEntrada):
    try:
        analisis = analizar_texto(datos.texto)

        return {
            "texto_original": datos.texto,
            "analisis": analisis.model_dump()
        }

    except RequestException:
        raise HTTPException(
            status_code=502,
            detail="No se pudo comunicar con el proveedor de IA"
        )

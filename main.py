
from fastapi import FastAPI, HTTPException
from requests import RequestException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from schemas import TextoEntrada
from llm_service import analizar_texto
from database import SessionLocal
from models import AnalisisRegistro

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

    # 1. TRANSFORM: analizar con IA
    try:
        analisis = analizar_texto(datos.texto)

    except RequestException:
        raise HTTPException(
            status_code=502,
            detail="Error de comunicación con OpenRouter"
        )

    except (ValidationError, ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="El LLM devolvió una respuesta inválida"
        )

    # 2. LOAD: guardar en PostgreSQL
    try:
        with SessionLocal() as db:
            registro = AnalisisRegistro(
                texto_original=datos.texto,
                resultado=analisis.model_dump()
            )

            db.add(registro)
            db.commit()
            db.refresh(registro)

            registro_id = registro.id

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar el análisis"
        )

    # 3. Responder al cliente
    return {
        "id": registro_id,
        "texto_original": datos.texto,
        "analisis": analisis.model_dump()
    }

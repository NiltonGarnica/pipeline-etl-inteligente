
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, HTTPException
from requests import RequestException
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from schemas import TextoEntrada
from llm_service import analizar_texto
from database import SessionLocal
from models import AnalisisRegistro


app = FastAPI(
    title="Pipeline ETL Inteligente",
    description="Microservicio para analizar narrativas con IA y PostgreSQL",
    version="1.0.0"
)
templates = Jinja2Templates(directory="templates")


# 1. ENDPOINT RAÍZ
@app.get("/")
def inicio():
    return {
        "mensaje": "Pipeline ETL Inteligente"
    }


# 2. ENDPOINT DE ESTADO
@app.get("/health")
def verificar_salud():
    return {
        "status": "ok",
        "service": "pipeline-etl-inteligente"
    }


# 3. ENDPOINT ETL: EXTRACT + TRANSFORM + LOAD
@app.post("/process")
def procesar_texto(datos: TextoEntrada):

    # EXTRACT: recibir el texto mediante Pydantic
    texto_original = datos.texto

    # TRANSFORM: analizar el texto con el LLM
    try:
        analisis = analizar_texto(texto_original)

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

    # LOAD: guardar texto y análisis en PostgreSQL
    try:
        with SessionLocal() as db:

            registro = AnalisisRegistro(
                texto_original=texto_original,
                resultado=analisis.model_dump()
            )

            db.add(registro)
            db.commit()
            db.refresh(registro)

            registro_id = registro.id

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar el análisis en PostgreSQL"
        )

    # RESPUESTA AL CLIENTE
    return {
        "id": registro_id,
        "texto_original": texto_original,
        "analisis": analisis.model_dump()
    }


# 4. ENDPOINT PARA CONSULTAR LOS REGISTROS
@app.get("/registros")
def listar_registros():

    try:
        with SessionLocal() as db:

            consulta = select(AnalisisRegistro).order_by(
                AnalisisRegistro.id.desc()
            )

            registros = db.scalars(consulta).all()

            return [
                {
                    "id": registro.id,
                    "texto_original": registro.texto_original,
                    "analisis": registro.resultado,
                    "fecha_creacion": registro.fecha_creacion
                }
                for registro in registros
            ]

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="No se pudieron consultar los registros"
        )
@app.get("/web", response_class=HTMLResponse)
def pagina_web(request: Request):
    with SessionLocal() as db:
        registros = db.scalars(
            select(AnalisisRegistro).order_by(
                AnalisisRegistro.id.desc()
            ).limit(50)
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"registros": registros}
        )


@app.get("/web/registros", response_class=HTMLResponse)
def historial_web(request: Request):
    with SessionLocal() as db:
        registros = db.scalars(
            select(AnalisisRegistro).order_by(
                AnalisisRegistro.id.desc()
            ).limit(50)
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="historial.html",
            context={"registros": registros}
        )


@app.post("/web/process", response_class=HTMLResponse)
def procesar_desde_web(
    request: Request,
    texto: str = Form(min_length=1)
):
    # Reutilizamos la lógica ETL existente.
    resultado = procesar_texto(TextoEntrada(texto=texto))

    return templates.TemplateResponse(
        request=request,
        name="resultado.html",
        context={"resultado": resultado}
    )

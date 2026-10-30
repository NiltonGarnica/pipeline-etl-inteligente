from typing import Literal

from pydantic import BaseModel, Field


class TextoEntrada(BaseModel):
    texto: str = Field(min_length=1)


class AnalisisTexto(BaseModel):
    categoria: str
    sentimiento: Literal[
        "positivo",
        "negativo",
        "neutro"
    ]
    urgencia: Literal[
        "baja",
        "media",
        "alta"
    ]
    resumen: str = Field(min_length=1)
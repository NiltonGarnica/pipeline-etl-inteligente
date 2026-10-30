import os
import requests

from dotenv import load_dotenv
from app.schemas.schemas import AnalisisTexto

load_dotenv(override=True)


def analizar_texto(texto: str) -> AnalisisTexto:
    api_key = os.environ["OPENROUTER_API_KEY"]
    modelo = os.environ["OPENROUTER_MODEL"]

    respuesta = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": modelo,
            "provider": {
                "require_parameters": True
            },
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Analiza la reseña de un cliente. "
                        "Devuelve categoría, sentimiento, "
                        "urgencia y un resumen breve."
                    )
                },
                {
                    "role": "user",
                    "content": texto
                }
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "analisis_texto",
                    "strict": True,
                    "schema": AnalisisTexto.model_json_schema()
                }
            }
        },
        timeout=60
    )

    respuesta.raise_for_status()

    contenido = respuesta.json()["choices"][0]["message"]["content"]

    return AnalisisTexto.model_validate_json(contenido)
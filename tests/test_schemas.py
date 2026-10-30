from app.schemas.schemas import AnalisisTexto

respuesta = {
    "categoria": "Laptops",
    "sentimiento": "positivo",
    "urgencia": "baja",
    "resumen": "Cliente satisfecho con su laptop"
}

analisis = AnalisisTexto.model_validate(respuesta)

print("Validación correcta")
print(analisis.model_dump())
from app.services.llm_service import analizar_texto

texto = "Compré una laptop en 7000 Bs y funciona excelente"

resultado = analizar_texto(texto)

print(resultado.model_dump_json(indent=2))
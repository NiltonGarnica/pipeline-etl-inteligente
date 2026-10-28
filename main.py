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

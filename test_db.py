from sqlalchemy import text
from database import engine

try:
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("SELECT 1")
        )

        print("Conexión exitosa:", resultado.scalar())

except Exception as error:
    print("Error de conexión:", error)
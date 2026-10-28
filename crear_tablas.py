from sqlalchemy import text, inspect
from database import engine
from models import Base,Categoria, Producto, AnalisisRegistro


with engine.connect() as conexion:
    resultado = conexion.execute(
        text("""
            SELECT
                current_database(),
                current_schema(),
                current_user
        """)
    )

    print("Conexion real:", resultado.fetchone())

print("Modelos:", list(Base.metadata.tables.keys()))

Base.metadata.create_all(bind=engine)

inspector = inspect(engine)

print("Tablas en public:", inspector.get_table_names(schema="public"))
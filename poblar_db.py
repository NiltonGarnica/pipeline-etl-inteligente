import random

from sqlalchemy import select
from database import SessionLocal
from models import Categoria, Producto

categorias = {
    "Laptops": (5000, 20000),
    "Celulares": (1000, 8000),
    "Monitores": (800, 5000),
    "Teclados": (100, 1000),
    "Mouse": (50, 500),
}

with SessionLocal() as db:
    for nombre, (minimo, maximo) in categorias.items():

        # Buscar si la categoría ya existe
        categoria = db.scalar(
            select(Categoria).where(
                Categoria.nombre == nombre
            )
        )

        # Crear la categoría si no existe
        if categoria is None:
            categoria = Categoria(nombre=nombre)
            db.add(categoria)
            db.flush()

        # Generar 3 productos por categoría
        for numero in range(1, 4):
            producto = Producto(
                nombre=f"{nombre} {numero}",
                precio=random.randint(minimo, maximo),
                categoria_id=categoria.id
            )

            db.add(producto)

    db.commit()

print("Categorías y productos guardados correctamente")
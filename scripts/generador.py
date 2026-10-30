import random

categorias = {
    "laptop": (5000, 20000),
    "celular": (1000, 8000),
    "monitor": (800, 5000),
    "teclado": (100, 1000),
    "mouse": (50, 500)
}

def generar_producto():
    categoria = random.choice(list(categorias.keys()))

    precio_minimo, precio_maximo = categorias[categoria]

    precio = random.randint(precio_minimo, precio_maximo)

    return {
        "categoria": categoria,
        "precio": precio
    }


if __name__ == "__main__":
    for i in range(5):
        print(generar_producto())
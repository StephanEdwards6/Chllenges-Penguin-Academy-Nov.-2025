# Crear una funcion que tenga parametros (filas, columnas)
# Crear una matriz (tablero)
# Ubicar la poosicion del gato y del raton en el tablero
# Posteriormente  crear una funion para imprimir tablero

# def crear_tablero (filas, columnas):
#     fila=5
#     columna=5
#     tablero = []
#     for _ in range(filas):
#         fila = []
#         for _ in range(columnas):
#             fila.append(".")
#         tablero.append(fila)
#     tablero[0][0]= 'R'
#     tablero[4][4]= 'G'
    
#     for fila in tablero:
#         print(" ".join(fila))

# crear_tablero(5,5)


def crear(filas, columnas):
    matriz = [["." for _ in range(columnas)] for _ in range(filas)]
    matriz [0][0]= 'R'
    matriz [4][4]= 'G'

    return matriz

def imprimir_tablero(matriz):
    for fila in matriz:
        print(" ".join(fila))

tablero = crear(5, 5)
imprimir_tablero(tablero)

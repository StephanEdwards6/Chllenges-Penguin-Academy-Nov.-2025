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

# Crear una matriz o tablero, no una tupla.
def crear_matriz(filas, columnas):
    matriz = [["." for _ in range(columnas)] for _ in range(filas)]
    matriz [0][0]= 'R'
    matriz [4][4]= 'G'

    return matriz

tablero = crear_matriz(5, 5)

# Funcion para imprimir el tablero.
def imprimir_tablero(matriz):
    for fila in matriz:
        print(" ".join(fila))
        
# Funcion para encontrar los simbolos dentro de mi tablero.
def encontrar_posicion(tablero, simbolo):
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            if tablero[fila][columna] == simbolo:
                return fila,columna
    return None

# Para que los personajes no se salgan del tablero
def movimientos_validos(tablero, fila, columna):
    movimientos =[
        (fila-1, columna), # arriba
        (fila+1, columna), # abajo
        (fila, columna-1), # izquierda
        (fila, columna+1), #derecha
    ]

    filas = len(tablero)
    columnas = len(tablero[0])
    
    return [(numero_de_fila, numero_de_columna) for numero_de_fila, numero_de_columna in movimientos
            if 0 <= numero_de_fila < filas and 0 <= numero_de_columna < columnas ]

# distancia = |fila1 - fila2| + |columna1 - columna2|

# Heuristica en este caso distancia Manhattan.
def heuristica(tablero):
    pos_raton = encontrar_posicion(tablero, 'R')
    pos_gato = encontrar_posicion(tablero, 'G')

    if pos_raton is None or pos_gato is None:
        return 0
    
    fila_del_raton, columna_del_raton = pos_raton
    fila_del_gato, columna_del_gato = pos_gato

    distancia = abs(fila_del_gato - fila_del_raton) + abs(columna_del_raton - columna_del_gato)

    # Cat forcing mechanic (tipo “taunt/agro” en WoW):
    if distancia == 1:
        return 1000   # Forzamos al gato a rematar
    else:
        return -distancia


def mover_raton_jugador(tablero):
    fila_actual, col_actual = encontrar_posicion(tablero, 'R')
    movimiento = input("Mover ratón (w=arriba, s=abajo, a=izquierda, d=derecha): ")

    # 1. Calcular la nueva posición según WASD
    if movimiento == "w":
        nueva_fila, nueva_columna = fila_actual - 1, col_actual
    elif movimiento == "s":
        nueva_fila, nueva_columna = fila_actual + 1, col_actual
    elif movimiento == "a":
        nueva_fila, nueva_columna = fila_actual, col_actual - 1
    elif movimiento == "d":
        nueva_fila, nueva_columna = fila_actual, col_actual + 1
    else:
        print("Movimiento inválido, el ratón no se mueve.")
        return

    # 2. Límites del tablero (corregido)
    filas = len(tablero)
    columnas = len(tablero[0])

    if not (0 <= nueva_fila < filas and 0 <= nueva_columna < columnas):
        print("¡No puedes salir del tablero!")
        return

    # 3. Evitar casilla ocupada por el gato
    if tablero[nueva_fila][nueva_columna] == "G":
        print("¡No puedes moverte encima del gato!")
        return

    # 4. Mover el ratón correctamente (corregido)
    tablero[fila_actual][col_actual] = "."
    tablero[nueva_fila][nueva_columna] = "R"


def minimax(tablero, profundidad, turno_gato):
    # ---------------------
    # 1. CASOS BASE
    # ---------------------
    pos_raton = encontrar_posicion(tablero, 'R')
    pos_gato = encontrar_posicion(tablero, 'G')

    if pos_raton == pos_gato:
        return 9999, None   # el gato ganó

    if pos_raton is None or pos_gato is None:
        return -9999, None

    if profundidad == 0:
        return heuristica(tablero), None
    

    # ---------------------
    # 2. TURNO DEL GATO (MAX)
    # ---------------------
    if turno_gato:
        mejor_valor = -999999
        mejor_mov = None

        # turno del gato
        fila_del_gato, columna_del_gato = pos_gato

        for nf, nc in movimientos_validos(tablero, fila_del_gato, columna_del_gato):
                if (nf, nc) == pos_raton:  
                    return 9999, (nf, nc)   # captura instantánea


        fila_del_gato, columna_del_gato = pos_gato
        for nueva_fila, nueva_columna in movimientos_validos(tablero, fila_del_gato, columna_del_gato):
            copia = [fila[:] for fila in tablero]
            copia[fila_del_gato][columna_del_gato] = '.'
            copia[nueva_fila][nueva_columna] = 'G'

            valor, _ = minimax(copia, profundidad-1, False)

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = (nueva_fila, nueva_columna)

        return mejor_valor, mejor_mov

    # ---------------------
    # 3. TURNO DEL RATÓN (MIN)
    # ---------------------
    else:
        peor_valor = 999999
        peor_mov = None

        fila_del_raton, columna_del_raton = pos_raton
        for nueva_fila, nueva_columna in movimientos_validos(tablero, fila_del_raton, columna_del_raton):
            copia = [fila[:] for fila in tablero]
            copia[fila_del_raton][columna_del_raton] = '.'
            copia[nueva_fila][nueva_columna] = 'R'

            valor, _ = minimax(copia, profundidad-1, True)

            if valor < peor_valor:
                peor_valor = valor
                peor_mov = (nueva_fila, nueva_columna)

        return peor_valor, peor_mov
   

# Bucle principal
while True:
    imprimir_tablero(tablero)
    print()

    # mover ratón
    fila_del_raton, columna_del_raton = encontrar_posicion(tablero, 'R')
    # aquí pones tu input del jugador
    mover_raton_jugador(tablero)
    # mover gato con minimax
    _, mov = minimax(tablero, profundidad=3, turno_gato=True)
    if mov is not None:
        fila_del_gato, columna_del_gato = encontrar_posicion(tablero, 'G')
        nueva_fila, nueva_columna = mov
        tablero[fila_del_gato][columna_del_gato] = '.'
        tablero[nueva_fila][nueva_columna] = 'G'

    # verificar fin del juego
    if encontrar_posicion(tablero, 'G') == encontrar_posicion(tablero, 'R'):
        print("El gato atrapó al ratón.")
        break


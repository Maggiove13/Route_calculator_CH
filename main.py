from queue import PriorityQueue

# Definir la cantidad de filas y columnas de la matriz // Solicitar al usuario
row = int(input("Ingrese el número de filas: "))
cols = int(input("Ingrese el número de columnas: "))

# Crear la matriz usando listas de comprensión anidadas
matrix = [[0 for _ in range(cols)] for _ in range(row)]

# # Primero va a imprimir la matriz, con la cantidad de filas y columnas que se definió
# print("La matriz inicial es:")
# for cell in matrix:
#     print(cell)

# Función para solicitar al usuario la coordenada de inicio y la coordenada del Destino en la matriz
def define_inicio_destino(row, cols):
    """Definir los puntos de origen y el destino"""
    
    while True:
        try: 
            start = input("Agregue las coordenadas para el inicio (formato x,y): ")
            start_x, start_y = map(int, start.split(',')) #como lo ingresado por el user seria un string con comas
            #split es un metodo que divide una cadena de texto en subcadenas usando la coma como delimitador
            # map: es una funcion que aplica otra funcion, en este caso int, ya que convierte a la lista de texto en un numero entero
            if start_x < 0 or start_x >= row or start_y < 0 or start_y >= cols:
                print("Esta fuera de la matriz, elige otra coordenada.")
                continue

            end = input("Agregue las coordenadas para el lugar Destino (formato x,y): ")
            end_x, end_y = map(int, end.split(',')) # divide la entrada y convierte a entero
            if end_x < 0 or end_x >= row or end_y < 0 or end_y >= cols:
                print("Esta fuera de la matriz, elige otra coordenada.")
                continue
            
            return (start_x, start_y), (end_x, end_y) # retorna las coordenadas de inicio y fin
        
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar las coordenadas en el formato correcto. Ej: 1,2 ")

# Llamar a la función para ubicar las coordenadas de inicio y fin
inicio, destino = define_inicio_destino(row, cols)

# Actualizar la matriz con las nuevas ubicaciones
matrix[inicio[0]][inicio[1]] = 1
matrix[destino[0]][destino[0]] = 2

# Ahora recorrer cada celda para imprimir la ubicacion de los elementos marcados por el usuario
# Reemplazar los ceros por puntos al imprimir la matriz
print("Matriz con los puntos de inicio y Destino, definidos: ")
for x in range(row):
    for y in range(cols):
        if matrix[x][y] == 1:
            print('I', end=' ')
        elif matrix[x][y] == 2:
            print('D', end=' ')
        else:
            print('.', end=' ')
    print()


#Ahora debemos agregar los obstaculos
#Función para agregar obstáculos a la matriz
def obstaculos(row, cols):
    """El usuario debe ingresar los obstaculos"""
    while True:
        try:
            barrier_input = input("Ingresa las coordenadas del obstáculo en formato: x, y (ingresa 'q' para salir): ")
            if barrier_input.lower() == 'q':
                break

            barrier_x, barrier_y = map(int, barrier_input.split(','))  # Convertir las coordenadas a enteros
            if barrier_x < 0 or barrier_x >= row or barrier_y < 0 or barrier_y >= cols:
                print("Está fuera de la matriz, elige otra coordenada.")
                continue

            # Verificar si la posición ya está ocupada por el inicio o el Destino
            elif matrix[barrier_x][barrier_y] in (1, 2):
                print("No se puede colocar un obstáculo en el inicio o el Destino.")
                continue

            matrix[barrier_x][barrier_y] = 'X'  # Marcamos el obstáculo con 'X'

            # Imprimir la matriz actualizada con los puntos de inicio, Destino y obstáculos
            print("Matriz con los puntos de inicio, Destino, y obstáculos definidos:")
            for x in range(row):
                for y in range(cols):
                    if matrix[x][y] == 1:
                        print('I', end=' ')
                    elif matrix[x][y] == 2:
                        print('D', end=' ')
                    elif matrix[x][y] == 'X':
                        print('X', end=' ')
                    else:
                        print('.', end=' ')
                print()

        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar las coordenadas en el formato correcto. Ej: 1,2")

# Llamar a la función para agregar obstáculos
obstaculos(row, cols)

#Funcion para calcular la heuristica:
def h_score(actual_cell, destino):
    """Calculo distancia Manhattan entre la celda que analice hasta la celda Destino"""
    x1, y1 = actual_cell
    end_x, end_y = destino #Este debe ser las celdas Destino
    
    return abs(x1 - end_x) + abs (y1 - end_y)


def A_star(matrix, inicio, destino):
    """Algoritmo A star"""
    # Crear un tablero con todos los nodos con valor (inf)
    f_score = { (x, y): float("inf") for x in range(row) for y in range(cols) }
    g_score = { (x, y): float("inf") for x in range(row) for y in range(cols) }
    g_score[inicio] = 0  # El costo de llegar al nodo inicial es 0

    # Calcular el valor de la celda inicial
    f_score[inicio] = h_score(inicio, destino)  # F = g+h
    fila = PriorityQueue()  # Crear una instancia de PriorityQueue
    #Crea una cola de prioridad fila que almacenará las celdas a explorar, priorizando aquellas con el menor valor F.
    fila.put((f_score[inicio], inicio))  # Añade la celda inicial a la cola con su valor F
    #El primer elemento es el valor f de la celda. el (f_score de inicio)
    #El segundo elemento es la celda en sí (una tupla de coordenadas). inicio

    # Almacenar la información de cuál es el mejor camino
    path = {}

    # Caminar a partir de la celda inicial explorando los próximos caminos
    # Mientras que la cola no este vacia
    while not fila.empty(): #El bucle continúa hasta que la cola esté vacía.
        current_f, cell = fila.get() # Obtiene el nodo con el valor f más bajo de la cola, current_f es el valor f y cell son las coordenadas de la celda.
        #Esta tupla contiene dos elementos: current_f y cell.
        # y con fila..get obtenes esos valores

        if cell == destino:
            break  # Salir del bucle si se llega al destino

        # Definir los movimientos posibles
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
        
        for direccion in direcciones: #Para cada dirección, calcula las coordenadas de la siguiente celda
            next_cell = (cell[0] + direccion[0], cell[1] + direccion[1])  # Determinar la siguiente celda
            
            # Verificar que la celda siguiente está dentro de los límites y no es un obstáculo
            if 0 <= next_cell[0] < row and 0 <= next_cell[1] < cols and matrix[next_cell[0]][next_cell[1]] != 'X':
                new_g = g_score[cell] + 1  # Se define el costo del camino a 1
                new_f = new_g + h_score(next_cell, destino) # Se calcula el valor F, de la celda adyacente que es F = G + H

                if new_f < f_score[next_cell]:  # Si la F de la celda adyacente es menor a la ya calculada 
                    f_score[next_cell] = new_f #entonces se actualiza el valor del costo, F de la celda.
                    g_score[next_cell] = new_g #entonces se actualiza el valor de g
                    fila.put((new_f, next_cell)) #Y añadimos la nueva celda a la fila con su costo F
                    path[next_cell] = cell  # Registrar el mejor camino hacia la siguiente celda en el diccionario Path

    # Reconstruir el camino a partir del destino. 
    #Para ello debemos ir en reversa
    #Comienza desde el destino y sigue el diccionario path hacia atrás hasta llegar al inicio.
    final_path = []
    cell = destino
    while cell != inicio:
        #Añade cada celda a la lista de camino final
        final_path.append(cell)
        cell = path.get(cell, inicio)  #obtiene la celda desde la que se llegó a cell. Si no existe, retorna inicio.

    final_path.append(inicio) #Añade la celda de inicio a la lista final_path.
    final_path.reverse()  # Invertir el camino para que vaya desde el inicio hasta el destino

    return final_path #La funcion me debe devolver la respuesta, osea el resultado final

# Ejecutar el algoritmo A* y obtener la ruta
ruta = A_star(matrix, inicio, destino)

# Actualizar la matriz con el camino encontrado
for cell in ruta:
    if cell != inicio and cell != destino:
        matrix[cell[0]][cell[1]] = '*'

# Imprimir la matriz final con el camino marcado
print("Matriz con el camino encontrado:")
for x in range(row):
    for y in range(cols):
        if matrix[x][y] == 1:
            print('I', end=' ')
        elif matrix[x][y] == 2:
            print('D', end=' ')
        elif matrix[x][y] == 'X':
            print('X', end=' ')
        elif matrix[x][y] == '*':
            print('*', end=' ')
        else:
            print('.', end=' ')
    print()

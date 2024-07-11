from queue import PriorityQueue

class Mapa2D():
    def __init__(self, row, cols, start, end):
        self.row = row
        self.cols = cols
        self.start = start
        self.end = end
        
        #Crearemos la matriz con listas de compresion anidadas
        self.matrix = [[0 for _ in range(cols)] for _ in range(row)]
        
        #Les vamos a asignar un valor a el inicio y el destino
        self.matrix[start[0]][start[1]] = 1
        self.matrix[end[0]][end[1]] = 2
        
        #Quiero que el metodo init pueda imprimir la matriz con los puntos de inicio y destino, definidas por el usuario
        # Ahora recorrer cada celda para imprimir la ubicacion de los elementos marcados por el usuario
        # Reemplazar los ceros por puntos al imprimir la matriz
        print("Matriz con los puntos de inicio y Destino, definidos: ")
        for x in range(self.row):
            for y in range(self.cols):
                if self.matrix[x][y] == 1:
                    print('I', end=' ')
                elif self.matrix[x][y] == 2:
                    print('D', end=' ')
                else:
                    print('.', end=' ')
            print()


    #Metodo para validar la entrada de las coordenadas de inicio(start) y destino(end)
    #Mientras la entrada sea valida va a continuar solicitando entrada al usuario
    #Este tipo de método no tiene acceso a la instancia (self) ni a la clase (cls), solo a los parámetros que se le pasan directamente. 
    # la lógica del método solo necesita los valores row y cols para validar las coordenadas, no necesita acceso a self.
    
    @staticmethod
    def valid_coordinates(row, cols): 
        while True:
            try:
                start = input("Agregue las coordenadas para el inicio de esta matriz de 5x5 (formato x,y): ")
                start_x, start_y = map(int, start.split(','))#como lo ingresado por el user seria un string con comas
                #split es un metodo que divide una cadena de texto en subcadenas usando la coma como delimitador
                # map: es una funcion que aplica otra funcion, en este caso int, ya que convierte a la lista de texto en un numero entero
                if start_x < 0 or start_x >= row or start_y < 0 or start_y >= cols:
                    print("Esta fuera de la matriz, elige otra coordenada.")
                    continue
                
                end = input("Agregue las coordenadas del Destino de esta matriz de 5x5 (formato x,y): ")
                end_x, end_y = map(int, end.split(',')) # divide la entrada y convierte a entero
                if end_x < 0 or end_x >= row or end_y < 0 or end_y >= cols:
                    print("Esta fuera de la matriz, elige otra coordenada.")
                    continue

                return (start_x, start_y), (end_x, end_y)

            except ValueError:
                print("Entrada inválida. Asegúrate de ingresar las coordenadas en el formato correcto. Ej: 1,2 ")

    #Metodo para solicitar al usuario que agregue coordenadas para los obstaculos
    def put_obstacles(self):
        while True:
            try:
                #Solicitar al usuario la entrada de coordenadas para una barrera
                barrier_input = input("Ingresa las coordenadas del obstáculo en formato: x, y (ingresa 'q' para salir): ")
                if barrier_input.lower() == 'q':
                    break
                
                # Con tuple convierte a tupla
                self.barrier = tuple(map(int, barrier_input.split(',')))

                if self.barrier[0] < 0 or self.barrier[0] >= self.row or self.barrier[1] < 0 or self.barrier[1] >= self.cols:
                    print("Está fuera de la matriz, elige otra coordenada.")
                    continue

                elif self.matrix[self.barrier[0]][self.barrier[1]] in (1, 2):
                    print("No se puede colocar un obstáculo en el inicio o el Destino.")
                    continue

                self.matrix[self.barrier[0]][self.barrier[1]] = 'X'
                
                # Imprimir la matriz actualizada con los puntos de inicio, Destino y obstáculos, cada vez que el usuario agregue un obstaculo
                print("Matriz con los puntos de inicio, Destino, y obstáculos definidos:")
                for x in range(self.row):
                    for y in range(self.cols):
                        if self.matrix[x][y] == 1:
                            print('I', end=' ')
                        elif self.matrix[x][y] == 2:
                            print('D', end=' ')
                        elif self.matrix[x][y] == 'X':
                            print('X', end=' ')
                        else:
                            print('.', end=' ')
                    print()

            except ValueError:
                print("Entrada inválida. Asegúrate de ingresar las coordenadas en el formato correcto. Ej: 1,2")


    #Metodo para imprimir la matriz con el inicio, fin y obstaculos marcados
    def print_matrix(self):
        print('\n Ruta final encontrada!! :) \n')
        for x in range(self.row):
            for y in range(self.cols):
                if self.matrix[x][y] == 1:
                    print('I', end=' ')
                elif self.matrix[x][y] == 2:
                    print('D', end=' ')
                elif self.matrix[x][y] == 'X':
                    print('X', end=' ')
                elif self.matrix[x][y] == '*':
                    print('*', end=' ')
                else:
                    print('.', end=' ')
            print()
        print('\n')


class RouteCalculator(Mapa2D):
    def __init__(self, row, cols, start, end):
        super().__init__(row, cols, start, end)
        
        #Este es el metodo constructor: cada vez que instanciemos RouteCalculator, los valores F de todas las celdas serà infinito
        self.f_score = { (x, y): float("inf") for x in range(self.row) for y in range(self.cols) }
        self.g_score = { (x, y): float("inf") for x in range(self.row) for y in range(self.cols) }
        
        #El resultado o camino, se guardará en esta lista vacia
        self.final_path = []
        
        #Acá definimos las variables start y end
        self.start = start
        self.end = end
        
        #Definimos primeramente el g de la celda inicial, que será 0
        self.g_score[start] = 0 
        
        # Y ahora calcularemos el valor de la celda inicial
        self.f_score[start] = self.g_score[start] + self.h_score(start, end)  # F = g+h
        
        self.q = PriorityQueue()  # Crear una instancia de PriorityQueue, osea el objeto q= de queue
        #Crea una cola de prioridad fila que almacenará las celdas a explorar, priorizando aquellas con el menor valor F.
        self.q.put((self.f_score[start], start))  # Añade la celda inicial a la cola con su valor F
        #El primer elemento es el valor f de la celda. el (f_score de inicio)
        #El segundo elemento es la celda en sí (una tupla de coordenadas). inicio

        # Almacenar la información de cuál es el mejor camino. Acceso a elementos mediante claves
        self.path = {} 
        #es un diccionario en el que las claves son celdas (coordenadas) y los valores son las celdas desde las que llegamos a esas claves. osea los padres

    #Metodo para calcular la heuristica, metodo temporal, se usa solo para el metodo Astar
    def h_score(self, current_cell, destino): #como no necesitamos acceder o modificar atributos de instancia, usamos parámetros locales.
        """Calculo distancia Manhattan entre la celda que analice hasta la celda destino"""
        x1, y1 = current_cell
        end_x, end_y = end #Este debe ser las celdas Destino
        
        return abs(x1 - end_x) + abs (y1 - end_y)


    #Metodo de encontrar la ruta
    def astar_route_finder(self):
        """Algoritmo A star"""
    
        # Caminar a partir de la celda inicial explorando los próximos caminos
        # Mientras que la cola no este vacia
        while not self.q.empty(): #El bucle continúa hasta que la cola esté vacía.
                current_f, cell = self.q.get() # Obtiene el nodo con el valor f más bajo de la cola, current_f es el valor f y cell son las coordenadas de la celda.
                #Esta tupla contiene dos elementos: current_f y cell.
                # y con fila..get obtenes esos valores

                if cell == self.end:
                    break  # Salir del bucle si se llega al destino

                # Definir los movimientos posibles
                direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
                
                for direccion in direcciones: #Para cada dirección, calcula las coordenadas de la siguiente celda
                    next_cell = (cell[0] + direccion[0], cell[1] + direccion[1])  # Determinar la siguiente celda
                    
                    # Verificar que la celda siguiente está dentro de los límites y no es un obstáculo
                    if 0 <= next_cell[0] < self.row and 0 <= next_cell[1] < self.cols and self.matrix[next_cell[0]][next_cell[1]] != 'X':
                        new_g = self.g_score[cell] + 1  # Se define el costo del camino a 1
                        new_f = new_g + self.h_score(next_cell, self.end) # Se calcula el valor F, de la celda adyacente que es F = G + H

                        if new_f < self.f_score[next_cell]:  # Si la F de la celda adyacente es menor a la ya calculada 
                            self.f_score[next_cell] = new_f #entonces se actualiza el valor del costo, F de la celda.
                            self.g_score[next_cell] = new_g #entonces se actualiza el valor de g
                            self.q.put((new_f, next_cell)) #Y añadimos la nueva celda a la fila con su costo F
                            self.path[next_cell] = cell  # Registrar el mejor camino hacia la siguiente celda en el diccionario Path

            # Reconstruir el camino a partir del destino. 
            #Para ello debemos ir en reversa
            #Comienza desde el destino y sigue el diccionario path hacia atrás hasta llegar al inicio.
                self.final_path = []
                cell = self.end # La celda actual se establece inicialmente como la celda de destino para poder reconstruir el camino desde el destino hasta el inicio. 
                while cell != self.start:
                #Añade cada celda a la lista de camino final
                    self.final_path.append(cell)
                    cell = self.path.get(cell, self.start)  #obtiene la celda desde la que se llegó a cell. Si no existe, retorna inicio.

                self.final_path.append(self.start) #Añade la celda de inicio a la lista final_path.
                self.final_path.reverse()  # Invertir el camino para que vaya desde el inicio hasta el destino

        return self.final_path #La funcion me debe devolver la respuesta, osea el camino final

    #Metodo para imprimir la ruta -----> Ejecutar el algoritmo A* y obtener la ruta
    def resultado_ruta(self):
        
        ruta = self.astar_route_finder()

        # Actualizar la matriz con el simbolo para el camino
        for cell in ruta:
            if cell != self.start and cell != self.end:
                self.matrix[cell[0]][cell[1]] = '*'

        #Ahora para imprimir el camino
        self.print_matrix() #llamamos al metodo creado en Mapa2D, para imprimir la matriz


#Definir la cantidad de filas y columnas
row = 5
cols = 5

# Validar las coordenadas de inicio y fin
start, end = Mapa2D.valid_coordinates(row, cols)

#Instanciamos la clase para crear un objeto: el objeto MAZE
maze = RouteCalculator(row, cols, start, end)
maze.put_obstacles()
maze.resultado_ruta()


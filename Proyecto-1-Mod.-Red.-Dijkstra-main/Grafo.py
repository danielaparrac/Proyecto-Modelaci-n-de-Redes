import numpy as np

class Graph:
    # matriz de adyacencia 36x36 con 0 en todas sus posiciones (Hay 36 nodos)
    adjMatrix = np.zeros((36, 36))

    def __init__(self):
        ''' Se inicializa la matriz de adyacencia, que tendra el tiempo base que 
        tarda llegar de un nodo a otro, se deja en 0 el tiempo en llegar de un nodo a si mismo y 
        asigna 999 en las otras posiciones, porque muchos nodos no tienen una arista en comun'''
        for i in range(0, 36):
            for j in range(0, 36):
                # if(i != j):
                self.adjMatrix[i][j] = 999
        self.initMatrix()

    def initMatrix(self):
        '''Como la matriz es simetrica, se rellena el cuadrante de abajo primero porque 
        sus coordenadas son mas faciles de leer en relacion a la cuadricula y 
        luego con el se rellena el cuadrante superior'''

        # Se rellena el tiempo para las carreras
        for i in range(0, 30):
            # Se asigna el tiempo de las aristas que forman las carreras 12, 13 y 14            
            if(i == 2 or i == 3 or i == 4 or i == 8 or i == 9 or i == 10 or i == 14 or i == 15 or i == 16
                    or i == 20 or i == 21 or i == 22 or i == 26 or i == 27 or i == 28):
                self.adjMatrix[i][i+6] = 7
            # Y de las aristas que forman las otras carreras
            else:
                self.adjMatrix[i][i+6] = 5

        # Se rellena el tiempo para las calles
        for i in range(0, 35):
            # Se asigna el tiempo de las aristas que forman la calle 51
            if(i in range(6, 11)):
                self.adjMatrix[i][i+1] = 10
            # Y de las aristas que forman las otras calles 
            elif(i != 5 and i != 11 and i != 17 and i != 23 and i != 29):
                self.adjMatrix[i][i+1] = 5

        # Se hace la equivalencia del cuadrante de abajo relleno con el de arriba
        for i in range(36):
            for j in range(i, 36):
                self.adjMatrix[j][i] = self.adjMatrix[i][j]


    def initInfoMatrix(self, initialNode):
        ''' Se crea la matriz de informacion Nodo | Tiempo min desde origen | Predecesor
        que sera necesaria para aplicar el algoritmo Dijkstra'''
        infoMatrix = np.zeros((36, 3))
        index = 0

        # Se asigna el nombre de los nodos
        for i in range(36):
            if (index == 6):
                index = 0

            if i in range(6):
                infoMatrix[i][0] = 5010 + index

            elif i in range(6, 12):
                infoMatrix[i][0] = 5110 + index

            elif i in range(12, 18):
                infoMatrix[i][0] = 5210 + index

            elif i in range(18, 24):
                infoMatrix[i][0] = 5310 + index

            elif i in range(24, 30):
                infoMatrix[i][0] = 5410 + index

            else:
                infoMatrix[i][0] = 5510 + index

            index += 1

        # Se inicializa el tiempo minimo en llegar del nodo de inicio a todos los otros
        # en un numero muy grande (999)
        for i in range(36):
            infoMatrix[i][1] = 999

        # Se coloca en 0 el tiempo en llegar del nodo inicio a si mismo
        infoMatrix[initialNode][1] = 0

        return infoMatrix

    def dijkstra(self, start, end):
        ''' Se aplica el algoritmo de Dijkstra para buscar el camino de costo minimo entre 
        dos nodos'''

        # Se toma como nodo de inicio en el que vive Javier
        if(start == 5414.0):
            infoMatrix = self.initInfoMatrix(28)
        # O se toma como nodo de inicio en el que vive Andreina
        else:
            infoMatrix = self.initInfoMatrix(15)

        prev = 0

        # Se crea el array que contendra los nodos que aun no hayan sido visitados
        notVisited = []

        for i in range(36):
            notVisited.append(infoMatrix[i][0])
        # Mientras hayan nodos no visitados
        while(len(notVisited) != 0):

            minDistance = 999

            # Se busca el nodo no visitado mas cercano al nodo de inicio
            for i in range(36):

                if(infoMatrix[i][0] in notVisited):

                    if(infoMatrix[i][1] < minDistance):
                        minDistance = infoMatrix[i][1]
                        node = infoMatrix[i][0]

            # Se procede a visitar el nodo hallado mas cercano al inicio
            for i in range(36):
                # Se busca el nodo
                if(infoMatrix[i][0] == node):
                    # Se visita y por lo tanto se saca de la matriz de no visitados
                    notVisited.remove(node)
                    # Se guarda su predecesor
                    prev = node

                    # Se examinan sus nodos adyacentes no visitados
                    for j in range(36):
                        # if(infoMatrix[j][0] in notVisited and self.adjMatrix[i][j] != 999):
                        if(self.adjMatrix[i][j] != 999):
                            # Si suma de tiempo del nodo inicio al nodo actual y tiempo 
                            # del nodo actual al nodo adyacente es menor que tiempo de 
                            # nodo inicio a nodo adyacente en la tabla
                            if(infoMatrix[j][1] > self.adjMatrix[i][j] + minDistance):
                                # Se actualiza el tiempo y predecesor en la tabla
                                infoMatrix[j][1] = minDistance + self.adjMatrix[i][j]

                                infoMatrix[j][2] = prev

        return self.getRoute(infoMatrix, start, end)

    def getRoute(self, infoMatrix, start, destiny):
        '''Se reconstruye el camino de costo minimo de un nodo inicio a un nodo destino'''

        output = int(destiny)
        aux = destiny
        time = []

        while(aux != start):
            for i in range(36):
                # Se busca en la matriz de informacion el nodo actual
                if(infoMatrix[i][0] == aux):

                    if(destiny == infoMatrix[i][0]):
                        minutes = infoMatrix[i][1]
                    # Se actualiza el nodo actual al predecesor del mismo
                    aux = infoMatrix[i][2]

                    # Para quitarle los decimales
                    newPoint = int(aux)
                    time.insert(0, infoMatrix[i][1])

                    # Se agrega el nodo actual a la cadena que se encarga de reconstruir 
                    # el camino final
                    output = str(newPoint) + " --> " + str(output)
                    
                    # Si se llega al nodo inicio, el camino esta completo
                    if(aux == start):
                        break

        time.insert(0, 0)

        return ({
            'route': output,
            'minutes': minutes,
            'time': time
        })

    def updateAdjMatrix(self, arrayRoute):
        ''' Se elimina una ruta de la matriz de adyacencia'''

        coors = []

        for coord in arrayRoute:
            coors.append(coord[1] + coord[3])

        # Se actualiza la matriz adyacente de forma que aquellas aristas que hayan sido 
        # recorridas por Javier no puedan ser recorridas por Andreina el zip esta corrido 
        # en coors, coors[1:] porque se necesita es la interseccion entre 2 nodos consecutivos 
        # en el camino para actualizar en la matriz
        for x, y in zip(coors, coors[1:]):

            if int(x[0]) == 0:
                coorX = 0
            elif int(x[0]) == 1:
                coorX = 6
            elif int(x[0]) == 2:
                coorX = 12
            elif int(x[0]) == 3:
                coorX = 18
            elif int(x[0]) == 4:
                coorX = 24
            else:
                coorX = 30

            if int(y[0]) == 0:
                coorY = 0
            elif int(y[0]) == 1:
                coorY = 6
            elif int(y[0]) == 2:
                coorY = 12
            elif int(y[0]) == 3:
                coorY = 18
            elif int(y[0]) == 4:
                coorY = 24
            else:
                coorY = 30

            self.adjMatrix[coorX+int(x[1])][(coorY+int(y[1]))] = 999

    def updateMatrixTo(self, num):
        ''' Actualiza todas las posiciones de la matriz de adyacencia sumandole un numero'''
        for i in range(0, 36):
            for j in range(0, 36):
                if(self.adjMatrix[i][j] != 999):
                    self.adjMatrix[i][j] += num
                    

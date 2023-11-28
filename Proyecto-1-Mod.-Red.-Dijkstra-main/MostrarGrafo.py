import networkx as nx
import matplotlib.pyplot as plt


def ShowGraph(ruta_javier, ruta_andreina, title):
    # Se crea el grafo
    g = nx.Graph()

    # Se agregan los nodos en su posicion correspondiente
    carrera = 15

    for i in range(6):
        calle = 50
        for j in range(6):

            g.add_node(str(calle) + str(carrera), pos=(i, j))

            calle += 1

        carrera -= 1

    # Se agregan las aristas entre sus nodos adyacentes
    calle = 50
    carrera = 15

    for i in range(6):
        calle = 50
        carreraW = 5
        if carrera in (12, 13, 14):
            carreraW = 7

        for j in range(6):
            calleW = 5
            if calle == 51:
                calleW = 10
            if carrera - 1 >= 10:
                g.add_edge(str(calle) + str(carrera), str(calle) +
                           str(carrera - 1),  weight=calleW)

            if calle + 1 <= 55:
                g.add_edge(str(calle) + str(carrera),
                           str(calle + 1) + str(carrera),  weight=carreraW)

            calle += 1

        carrera -= 1

    # print(g.nodes(data=True))
    # print(g.edges(data=True))

    pos = nx.get_node_attributes(g, 'pos')
    edgeLabels = nx.get_edge_attributes(g, 'weight')

    # javier = 5414
    # andreina = 5213
    theDarkness = "5014"
    laPasion = "5411"
    miRolita = "5012"
    cafeSensacion = "5411"

    # Definiendo estilos para las aristas
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edgeLabels, font_size=9)
    nx.draw(g, pos, with_labels=True, node_size=750,
            width=2, font_size=10, node_color="#ffe5d9")

    # Definiendo estilos para lugares de encuentro
    nx.draw_networkx_nodes(g, pos, nodelist=[
                           theDarkness, laPasion, miRolita, cafeSensacion], node_size=750, node_color="#9d8189")

    # Se construye el array de nodos por los que pasa Javier
    javierNodes = ruta_javier.split(" --> ")

    # Se construye el array de aristas por las que pasa Javier
    javierEdges = []

    for edge in g.edges(nbunch=javierNodes):
        if edge[0] in javierNodes and edge[1] in javierNodes:
            javierEdges.append(edge)

    # Se modifica el color del camino de Javier
    nx.draw_networkx_nodes(
        g, pos, nodelist=javierNodes[:-1], node_size=750, node_color="#d8e2dc")
    nx.draw_networkx_edges(g, pos, edgelist=javierEdges,
                           edge_color="#d8e2dc", width=2)

    # Se construye el array de nodos por los que pasa Andreina
    andreinaNodes = ruta_andreina.split(" --> ")

    # Se construye el array de aristas por las que pasa Andreina
    andreinaEdges = []

    for edge in g.edges(nbunch=andreinaNodes):
        if edge[0] in andreinaNodes and edge[1] in andreinaNodes:
            andreinaEdges.append(edge)

    # Se modifica el color del camino de Andreina
    nx.draw_networkx_nodes(
        g, pos, nodelist=andreinaNodes[:-1], node_size=750, node_color="#ffcad4")
    nx.draw_networkx_edges(g, pos, edgelist=andreinaEdges,
                           edge_color="#ffcad4", width=2)

    # Se agrega el titulo
    plt.title(title, fontsize=11)

    # Se muestra el grafo
    plt.show()

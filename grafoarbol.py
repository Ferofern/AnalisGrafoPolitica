import networkx as nx
import matplotlib.pyplot as plt
import csv
from collections import Counter

recibidos = []
enviados = []
ciudades = []

with open('matriz.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        recibidos.append(row[0])
        enviados.append(row[1])
        ciudades.append(row[2])


# Creamos un multigrafo dirigido
G = nx.MultiDiGraph()

# Agregamos aristas dirigidas al multigrafo
for i in range(len(enviados)):
    G.add_edge(enviados[i], recibidos[i])

# Asignamos atributo 'ciudad' solo a los nodos que tengan información
ciudades_dict = {node: ciudades[i] for i, node in enumerate(recibidos)}
nx.set_node_attributes(G, ciudades_dict, name='ciudad')

# Imprimimos los nodos con sus grados en orden descendente
out_degree_dict = dict(G.out_degree(G.nodes()))  # Utilizamos out_degree() para contar las flechas de salida
sorted_out_degrees = sorted(out_degree_dict.items(), key=lambda x: x[1], reverse=True)


print("Nodos con más flechas de salida:")
for node, out_degree in sorted_out_degrees:
    if 1 < out_degree:
        ciudad = G.nodes[node].get('ciudad', 'Ciudad no disponible')  # Use get() with a default value
        print(f"{node} ({ciudad}): {out_degree} flechas de salida")


# Obtener el recorrido por profundidad desde un vértice específico
def dfs_from_vertex(graph, start_vertex):
    visited = set()
    stack = [start_vertex]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            ciudad = G.nodes[vertex].get('ciudad', 'Ciudad no disponible')  # Use get() with a default value
            print(f"{vertex} ({ciudad})")  # Imprimir el vértice visitado y la ciudad asociada
            neighbors = list(graph.neighbors(vertex))
            stack.extend(neighbors[::-1])

    return visited  # Devolvemos el conjunto de nodos visitados
start_vertex = 0

while start_vertex != 'detente':
    # Pide al usuario que ingrese el vértice inicial para el recorrido DFS
    start_vertex = input("Ingresa el nombre del vértice inicial para el recorrido DFS: ")

    # Verifica si el vértice ingresado existe en el grafo
    if start_vertex in G.nodes():
        # Realizar el recorrido por profundidad desde el vértice inicial
        print("Recorrido por profundidad desde el vértice", start_vertex)
        visited_nodes = dfs_from_vertex(G, start_vertex)

        # Contar las ciudades más repetidas
        city_counter = Counter(G.nodes[node]['ciudad'] for node in visited_nodes if 'ciudad' in G.nodes[node])

        # Ordenar las ciudades por frecuencia (de mayor a menor)
        sorted_cities = sorted(city_counter.items(), key=lambda x: x[1], reverse=True)

        print("Ciudades más repetidas:")
        for city, count in sorted_cities:
            print(f"{city}: {count}")

        # Dibujamos el multigrafo con el recorrido DFS resaltado en rojo
        pos = nx.spring_layout(G, seed=42)

        # Color de los nodos
        node_colors = ['red' if node in visited_nodes else 'skyblue' for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=200, node_shape='o')

        # Color de las aristas
        edge_colors = ['red' if (u, v) in G.edges() and u in visited_nodes and v in visited_nodes else 'gray' for u, v in
                       G.edges()]
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowsize=4)

        # Etiquetas de los nodos con tamaño de fuente personalizado
        labels = {node: f"{node}\n({G.nodes[node].get('ciudad', 'Ciudad no disponible')})" if node in visited_nodes else "" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_weight='bold')

        # Mostramos el multigrafo con el recorrido DFS resaltado en rojo
        plt.title("Grafo/Arbol Individual")
        plt.show()
    else:
        print("El vértice ingresado no existe en el grafo.")

lista = recibidos + enviados

lista = set(lista)

for elemento in lista:
    print(elemento)
print(len(lista))

recibidos = set(recibidos)

print('Personas que han llenado: ',len(recibidos))
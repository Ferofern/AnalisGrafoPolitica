import networkx as nx
import matplotlib.pyplot as plt
import csv

def contar_elementos_repetidos(lista):
    contador = {}
    for elemento in lista:
        contador[elemento] = lista.count(elemento)
    return contador


recibidos = []
enviados = []
ciudades = []

with open('matriz.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        recibidos.append(row[0])
        enviados.append(row[1])
        ciudades.append(row[2].strip())

G = nx.MultiDiGraph()

for ciudad in set(recibidos):
    if ciudad:
        G.add_node(ciudad)


for i, ciudad in enumerate(recibidos):
    if ciudades[i]:
        G.nodes[ciudad]['ciudad'] = ciudades[i]

for i in range(len(enviados)):
    G.add_edge(enviados[i], recibidos[i])

ciudad_count = {}
for ciudad in ciudades:
    if ciudad:
        ciudad_count[ciudad] = ciudad_count.get(ciudad, 0) + 1
sorted_ciudades = sorted(ciudad_count.items(), key=lambda x: x[1], reverse=True)

sorted_out_degrees = sorted(G.out_degree(), key=lambda x: x[1], reverse=True)
print("Nodos con más flechas de salida:")
for node, out_degree in sorted_out_degrees:
    if node != 'COALICIÓN EL RESURGIR DE LA PATRIA':
        if 1 < out_degree:
            ciudad = G.nodes[node].get('ciudad', 'Ciudad no disponible')
            print(f"{node} ({ciudad}): {out_degree} flechas de salida")

pos = nx.spring_layout(G, seed=42)
labels = {node: f"{node} - {G.nodes[node].get('ciudad')}" for node in G.nodes()}
nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', font_size=8, font_weight='bold', arrowsize=4, labels=labels)

print('-----------------------')
resultado = contar_elementos_repetidos(ciudades)

for elemento, cantidad in resultado.items():
    print(f"{elemento}: {cantidad}")

plt.title("Multigrafo Dirigido")
plt.show()

lista = recibidos + enviados

lista = set(lista)

for elemento in lista:
    print(elemento)
print(len(lista))

recibidos = set(recibidos)

print('Personas que han llenado: ',len(recibidos))
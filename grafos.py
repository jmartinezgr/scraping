import networkx as nx
import random
grafo = {
    1:{2,3,4},
    2:{1,4,5},
    3:{1,5,6},
    4:{1,2,6},
    5:{2,3},
    6:{3,4}
}
G = nx.Graph()

G.add_nodes_from(grafo.keys())

print(G.nodes())

for clave,valor in grafo.items():
    for i in valor:
        G.add_edge(clave,i)


print(G.edges())

"""
grafo[1].add('xd')



if 'xd ' in grafo[1]:
    grafo[1].add('diis')

print(grafo[1])
"""



"""
lista_nuevas_claves = []
set_nuevo = set()
for i in range(10):
    nueva = random.randint(2,20)
    set_nuevo.add(nueva)
    if not(grafo.get(nueva,False)):
        lista_nuevas_claves.append(nueva)
        grafo[nueva] = {1}
    
grafo[1] = set_nuevo

print(len(grafo.keys()))


for k in range(0,5):
for j in grafo.keys():
     
for i in grafo[1]:
    if not(grafo.get(i,False)):
        print(i,"no existe")
        lista_nuevas_claves.append(i)
        grafo[i] = {random.randint(1,10),random.randint(1,10),random.randint(1,10)}

for i in lista_nuevas_claves:
    pass

print(grafo.items())
print(lista_nuevas_claves)"""

"""
for i in range(len(lista_nuevos)):
    link = 'https://es.wikipedia.org/wiki/'+lista_nuevos[0]
    cajita = obtener_script_html(link=link)
    datos = limpiar_datos(cajita)
    dic,lista_nuevos = agregar_nodos(dic,datos,lista_nuevos[0],lista_nuevos)
"""

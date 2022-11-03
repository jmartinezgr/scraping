import random
grafo = {

}


lista_nuevas_claves = []
set_nuevo = set()
for i in range(10):
    nueva = random.randint(2,20)
    set_nuevo.add(nueva)
    if not(grafo.get(nueva,False)):
        lista_nuevas_claves.append(nueva)
        grafo[nueva] = {1}
    
grafo[1] = set_nuevo


"""
for k in range(0,5):
for j in grafo.keys():
     
for i in grafo[1]:
    if not(grafo.get(i,False)):
        print(i,"no existe")
        lista_nuevas_claves.append(i)
        grafo[i] = {random.randint(1,10),random.randint(1,10),random.randint(1,10)}

for i in lista_nuevas_claves:
    pass
"""
print(grafo.items())
print(lista_nuevas_claves)
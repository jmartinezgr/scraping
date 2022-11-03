from bs4 import BeautifulSoup
import requests
import time
import networkx as nx

def obtener_nombre():
    pass

def obtener_script_html(link):
    
    response = requests.get(link)
    soup = BeautifulSoup(response.text,'lxml')

    return soup.find('div',id='bodyContent')

def limpiar_datos(a_s):
    links = a_s.find_all('a')
    links_list = []
    lista_numeros = ['1','2','3','4','5','6','7','8','9'] 
    for i in links:
        text = i.get_text(strip=True,separator=' ')
        if len(text.split())>1 and len(text.split())<4:
            if text[0] != '[' and not(text[0] in lista_numeros) and text!= 'el original':
                links_list.append(i)
    return links_list

def obtener_links(link):
    return comprobar_entidad('https://es.wikipedia.org'+link.attrs.get('href'))


def comprobar_entidad(link):
    box = obtener_script_html(link)
    nacimiento = box.find_all('th')
    for i in nacimiento:
        if i.get_text() == 'Nacimiento':
            return True
    return False

def agregar_nodos(dic_nodos,datos,node,lista_nuevos,lista_revisados):
    
    if not dic_nodos.get(node,False):
        dic_nodos[node] = set()

    for i in datos:
        try:
            if obtener_links(i):
                dic_nodos[node].add(i.get_text())
                if not(dic_nodos.get(i,False)):
                    dic_nodos[i.get_text()] = {node}
                    if i.get_text() not in lista_revisados:
                        lista_nuevos.append(i.get_text())

        except:
            pass
    lista_revisados.append(lista_nuevos.pop(0))

    return dic_nodos,lista_nuevos,lista_revisados


time_initial = time.time()
dic = {}
lista_nuevos = ['Joe Biden']
lista_revisados = []

while len(dic)<=50 and len(lista_nuevos)>0:
    link = 'https://es.wikipedia.org/wiki/'+lista_nuevos[0]
    cajita = obtener_script_html(link=link)
    datos = limpiar_datos(cajita)
    dic,lista_nuevos,lista_revisados = agregar_nodos(dic,datos,lista_nuevos[0],lista_nuevos,lista_revisados)


G = nx.Graph()

G.add_nodes_from(dic.keys())


for clave,valor in dic.items():
    for i in valor:
        G.add_edge(clave,i)


print(G.edges())

print(list(nx.all_simple_paths(G,'Joe Biden','Antonio Villaraigosa')))

tiempo_final = time.time()
t = round(tiempo_final-time_initial,0)
t_s = f'{t//360}'
t = t-(t//360)
t_s = t_s+f':{t//60}:'
t = t- (t//60)
t_s = t_s+f'{t}'

print(f'Tiempo de ejecucion: {tiempo_final-time_initial}')
print(f'Tiempo de ejecucion en horas: {t_s}')
print(f'En el diccionario hay {len(dic)} elementos')
print(f'Nodos revisados: {len(lista_revisados)}')
print(f'Faltaron {len(lista_nuevos)} nodos nuevos por revisar')


print(dic['Joe Biden'])


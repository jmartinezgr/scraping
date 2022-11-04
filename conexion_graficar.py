from bs4 import BeautifulSoup
import requests
import time
import networkx as nx
import matplotlib.pyplot as plt

def guiones_bajos(clave):
    nuevo_nombre = clave.split()
    nn = nuevo_nombre[0]
    for i in range(1,len(nuevo_nombre)):
        nn+= '_'+nuevo_nombre[i]

    return nn

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def obtener_nombre():
    while True:
        x = input("Ingresa L si vas a ingresar un link o N si es un nombre: ")    
        if x in ('N','L'):
            clave = input('Ingresa la persona: ')
            if x == 'L':
                try:
                    if comprobar_entidad(clave):
                        nueva_clave = clave.split('/')[4]
                        return nueva_clave
                except:
                    print('Este link no existe en wikipedia')
            else:
                nn = guiones_bajos(clave=clave)
                try:
                    if comprobar_entidad('https://es.wikipedia.org/wiki/'+nn):
                        return clave
                except:
                    print('Este nombre no existe en wikipedia')
        else:
            print('Ingresa un tipo valido')

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

def agregar_nodos(dic_nodos,datos,node,lista_nuevos,lista_revisados,persona2,encontrar):

    for i in datos:
        try:
            if obtener_links(i):
                var = normalize(i.get_text())
                dic_nodos.add_node(var)
                dic_nodos.add_edge(node,var)
                #print(node,"-",var)
                if i.get_text() not in lista_revisados:
                    lista_nuevos.append(i.get_text())
                
                if persona2 in dic_nodos.nodes():
                    encontrar = True
                    break
            
        except:
            pass
    lista_revisados.append(lista_nuevos.pop(0))

    return dic_nodos,lista_nuevos,lista_revisados,encontrar

#Inicia el algoritmo

print("*** Vamos a ingresar la persona 1 ***")
persona1 = normalize(obtener_nombre())
print('***Vamos a ingresar a la persona 2 ***')
persona2 = normalize(obtener_nombre())

print('n/ Empezando la busqueda .. ... .... ')

encontrar = False

time_initial = time.time()
dic = nx.Graph()
lista_nuevos = [persona1]
lista_revisados = []

while len(dic)<=150 and len(lista_nuevos)>0 and encontrar == False:
    link = 'https://es.wikipedia.org/wiki/'+lista_nuevos[0]
    cajita = obtener_script_html(link=link)
    datos = limpiar_datos(cajita)
    dic,lista_nuevos,lista_revisados,encontrar = agregar_nodos(dic,datos,lista_nuevos[0],lista_nuevos,lista_revisados,persona2,encontrar)


#print(dic.edges())

if not encontrar:
    for i in range(len(lista_nuevos)):
        link = 'https://es.wikipedia.org/wiki/'+lista_nuevos[0]
        cajita = obtener_script_html(link=link)
        datos = limpiar_datos(cajita)
        dic,lista_nuevos,lista_revisados,encontrar = agregar_nodos(dic,datos,lista_nuevos[0],lista_nuevos,lista_revisados,persona2,encontrar)
        if encontrar == True:
            break

for j in dic.edges():
    print(f"Relacion: {j}")

if encontrar:
    ruta = list(nx.all_simple_paths(dic,persona1,persona2))
    string_ruta = ''
    for i in ruta[0]:
        string_ruta += i+"-> "
    print(string_ruta)
else:
    print('Relacion no encontrada')


tiempo_final = time.time()
#Calculo del tiempo en formato hh:mm:ss

t = round(tiempo_final-time_initial,0)
t_s = f'{t//3600}'
t = t-((t//3600)*3600)
t_s = t_s+f':{t//60}:'
t = t-((t//60)*60)
t_s = t_s+f'{t}'



#Dibujar un gráfico no dirigido
nx.draw(dic, with_labels=True, font_weight='bold')
plt.show()

import os
import errno
try:
    os.mkdir(f"/home/juan/Escritorio/Mycodes/scraping/pruebas/{guiones_bajos(persona1)}-{guiones_bajos(persona2)}")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


# guardar grafo
nx.write_graphml(dic, f"/home/juan/Escritorio/Mycodes/scraping/pruebas/{guiones_bajos(persona1)}-{guiones_bajos(persona2)}/{guiones_bajos(persona1)}_into_{guiones_bajos(persona2)}.graphml")

print(f'Tiempo de ejecucion: {tiempo_final-time_initial}')
print(f'Tiempo de ejecucion en horas: {t_s}')
print(f'En el diccionario hay {len(dic)} elementos')
print(f'Nodos revisados: {len(lista_revisados)}')
print(f'Faltaron {len(lista_nuevos)} nodos nuevos por revisar')
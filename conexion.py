from bs4 import BeautifulSoup
import requests
import time
import networkx as nx
import matplotlib.pyplot as plt

def segundos_a_segundos_minutos_y_horas(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

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
                nuevo_nombre = clave.split()
                nn = nuevo_nombre[0]
                for i in range(1,len(nuevo_nombre)):
                    nn+= '_'+nuevo_nombre[i]
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
                if not(i.get_text() in lista_nuevos):
                    lista_nuevos.append(i.get_text())
                
                if persona2 in dic_nodos.nodes():
                    encontrar = True
                    break
            
        except:
            pass
        
    lista_revisados.append(lista_nuevos.pop(0))

    return dic_nodos,lista_nuevos,lista_revisados,encontrar

#Inicia el algoritmo

persona1 = normalize(obtener_nombre())
persona2 = normalize(obtener_nombre())

print('*** Empezando la busqueda ***')

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
#t_s = segundos_a_segundos_minutos_y_horas(t)

print(f'Tiempo de ejecucion: {tiempo_final-time_initial}')
print(f'Tiempo de ejecucion en horas: {t_s}')
print(f'En el diccionario hay {len(dic)} elementos')
print(f'Nodos revisados: {len(lista_revisados)}')
print(f'Faltaron {len(lista_nuevos)} nodos nuevos por revisar')

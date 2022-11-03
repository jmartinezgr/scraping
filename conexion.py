from bs4 import BeautifulSoup
import requests

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

def agregar_nodos(dic_nodos,datos,node):
    set_nuevo_nodo = set()
    lista_nuevos = []
    for i in datos:
        try:
            if obtener_links(i):
                set_nuevo_nodo.add(i.get_text())
                if not(dic_nodos.get(i,False)):
                    dic_nodos[i.get_text()] = {node}
                    lista_nuevos.append(i.get_text())
            else:
                pass
                #print(i.get_text(), "no una persona")
        except:
            pass
            #print(i.get_text(), "no funciono el link")
    dic_nodos[node] = set_nuevo_nodo
    print(set_nuevo_nodo)
    print(lista_nuevos)
    return dic_nodos,lista_nuevos

cajita = obtener_script_html(link='https://es.wikipedia.org/wiki/Jorge_Oñate')
datos = limpiar_datos(cajita)
dic = {}
dic,lista_nuevos= agregar_nodos(dic,datos,"Jorge_Oñate")  

print(dic.items())

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

def agregar_nodos(datos):
    lista_nodos = []
    for i in datos:
        try:
            if obtener_links(i):
                #print(i.get_text(), "es una persona")
                if not(i in lista_nodos):
                    print(i.get_text())
                    lista_nodos.append(i)
            else:
                pass
                #print(i.get_text(), "no una persona")
        except:
            pass
            #print(i.get_text(), "no funciono el link")

cajita = obtener_script_html(link='https://es.wikipedia.org/wiki/Jorge_Oñate')
datos = limpiar_datos(cajita)
agregar_nodos(datos)


from bs4 import BeautifulSoup
import requests

website = 'https://es.wikipedia.org/wiki/Barack_Obama'
#website = 'https://es.wikipedia.org/wiki/Colombia'
#website = 'https://es.wikipedia.org/wiki/Diomedes_Diaz'
#website = 'https://es.wikipedia.org/wiki/Jorge_Oñate'


response = requests.get(website)

content = response.text

soup = BeautifulSoup(content,'lxml')

box = soup.find('div',id='bodyContent')
nacimiento = box.find_all('th')

link = box.find('a',title='Joe Biden')
print('https://es.wikipedia.org'+link.attrs.get('href'))
new='https://es.wikipedia.org'+str(link).split()[1].split('"')[1]

response = requests.get(new)

content = response.text

soup = BeautifulSoup(content,'lxml')

x = soup.find_all('th')


"""

link = box.find_all('a') 
print(len(link))

lista_numeros = ['1','2','3','4','5','6','7','8','9'] 
for i in link:
    text = i.get_text(strip=True,separator=' ')
    if len(text.split())>1 and len(text.split())<4:
        if text[0] != '[' and not(text[0] in lista_numeros) and text!= 'el original':
            print(i)
"""

for i in x:
    if i.get_text() == 'Nacimiento':
        print(True)
        break

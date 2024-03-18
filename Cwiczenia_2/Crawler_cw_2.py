import requests 
from bs4 import BeautifulSoup 
from urllib.parse import urljoin 
import random

def get_links(url): 
    response = requests.get(url) 
    bs = BeautifulSoup(response.text, 'html.parser') 
    links = bs.find_all('a', href=True) 
    absolutes = [] 
    for link in links:
        absolute_link = urljoin(url, link['href'])
        if absolute_link.startswith('http'):  # Filter out links with supported schemas
            absolutes.append(absolute_link)
    return absolutes 

def wylosuj(lista):
    wylosowany_element = random.choice(lista)
    return wylosowany_element

def main(): 
    website_url = 'https://www.onet.pl/'
    lista_wylosowanych_url = [website_url]
    k = 1
    while k <=100:   #wyświetla sie 3 linki
        links = get_links(website_url)  #zbieram linki ze strony
        # print(links)
        wylosowany_url = wylosuj(links)   #losuje jeden link ze strony
        while not get_links(wylosowany_url):
            wylosowany_url = wylosuj(links)
        website_url = wylosowany_url   #nowy adres url od którego znowu zaczniemy
        lista_wylosowanych_url.append(website_url)
        print(f"Iteration {k}: {website_url}") 
        k += 1
        
            
if __name__ == "__main__": 
    main()

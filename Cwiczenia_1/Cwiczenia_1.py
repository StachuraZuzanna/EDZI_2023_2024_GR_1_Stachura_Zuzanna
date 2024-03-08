import requests
import re
import unicodedata
from collections import Counter
from bs4 import BeautifulSoup

def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # mw-parser-output to klasa HTML uzywana na platformie MediaWiki - jest glownym kontenerem dla tresci
    content = soup.find('div', class_='mw-parser-output').text
    return content

def process_text(text):
    #Dopisz kod spelniajacy Punkt 2
    text = text.lower()   #małe litery
    text = re.sub(r'\b\d+\b|[^\w\s]','', text)  #wyrażenie regularne  
    text = ' '.join(text.split())

    return text

def get_ranked_words(text):
    ranked_words = None
    #Dopisz kod spelniajacy Punkt 3
    words = text.split(' ')  #podział tekstu na słowa.
    words = Counter(words)  #funkcja z modułu Connections
    ranked_words = words.most_common(100)
    return ranked_words

def write_results(results, filename):
    with open(filename, 'w') as file:
    #Dopisz kod spelniajacy Punkt 4
        file.write('ranking;słowo;ilosc wystapien\n')
        for i, (word, count) in enumerate(results, 1):
            file.write(f"{i};{word};{count}\n")


def main():
    url = 'https://en.wikipedia.org/wiki/Web_scraping'
    text = get_text(url)
    cleaned_text = process_text(text)
    final_words = get_ranked_words(cleaned_text)
    
    write_results(final_words, 'output.txt')

if __name__ == "__main__":
    main()
    
    

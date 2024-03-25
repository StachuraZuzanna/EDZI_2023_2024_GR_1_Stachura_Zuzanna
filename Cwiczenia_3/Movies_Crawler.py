import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def get_rotten_tomatoes_score(movie_title, release_year, base_url):
    search_url = f'{base_url}/search?search={movie_title.replace(" ", "+")}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('search-page-result', attrs={'type': 'movie'})
    for item in items:
        media_rows = item.find_all('search-page-media-row')
        for row in media_rows:
            release_year_row = row.get('releaseyear')
            if release_year_row == release_year:
                movie_title_row = row.find('a', class_='unset', attrs={'data-qa': 'info-name'}).text.strip()
                score = row.get('tomatometerscore')
                return movie_title_row, score
    return None, None

def get_text(url, base_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li', class_='ipc-metadata-list-summary-item')
    movies = []
    for item in items[:100]:
        title = item.find('h3', class_='ipc-title__text').get_text().split('. ')[1]
        metadata = item.find_all('span', class_='sc-b0691f29-8 ilsLEX cli-title-metadata-item')
        year = metadata[0].get_text(strip=True)
        imdb_rating = item.find('span', class_='ipc-rating-star--imdb').get('aria-label').split(': ')[1]
        ranking_place = item.find('h3', class_='ipc-title__text').get_text().split('.')[0]
        movie_title_row, score = get_rotten_tomatoes_score(title, year, base_url)
        movie_data = {'title': title, 'ranking':ranking_place,'ocena': imdb_rating,'rok':year, 'rotten_tomatoes_score': score}
        movies.append(movie_data)
        # print( movie_data )
    return movies

imdb_url = 'https://www.imdb.com/chart/top'
rotten_tomatoes_url = 'https://www.rottentomatoes.com'
movies_data = get_text(imdb_url, rotten_tomatoes_url)
# Zapisz wyniki do pliku JSON
with open('movies_data.json', 'w') as f:
    json.dump(movies_data, f, indent=4)

print("Dane zapisane do pliku 'movies_data.json'")

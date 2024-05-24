import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import logging

# MongoDB configuration
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'scrapethissite'
MONGO_COLLECTION = 'scrapedata'

# Logger configuration
logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR)

# Function to scrape data from the main URL
def scrape_main_url(url):
    try:
        response = requests.get("https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            data = []
            table = soup.find('table', class_='wikitable')  
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]: 
                    columns = row.find_all('td')
                    if len(columns) >= 4:
                        title = columns[0].text.strip()
                        nominations = columns[1].text.strip()
                        awards = columns[2].text.strip()
                        best_picture = columns[3].text.strip()
                        data.append({
                            'title': title,
                            'nominations': nominations,
                            'awards': awards,
                            'best_picture': best_picture
                        })
                return data
            else:
                logging.error(f"No table found on URL: {url}")
        else:
            logging.error(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error scraping URL: {url}. Error: {e}")

def scrape_second_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            data = []
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]:  
                    columns = row.find_all('td')
                    if len(columns) >= 9:
                        team_name = columns[0].text.strip()
                        year = columns[1].text.strip()
                        wins = columns[2].text.strip()
                        losses = columns[3].text.strip()
                        ot_losses = columns[4].text.strip()
                        win_percent = columns[5].text.strip()
                        gf = columns[6].text.strip()
                        ga = columns[7].text.strip()
                        plus_minus = columns[8].text.strip()
                        data.append({
                            'team_name': team_name,
                            'year': year,
                            'wins': wins,
                            'losses': losses,
                            'ot_losses': ot_losses,
                            'win_percent': win_percent,
                            'gf': gf,
                            'ga': ga,
                            'plus_minus': plus_minus
                        })
                return data
            else:
                logging.error(f"No table found on URL: {url}")
        else:
            logging.error(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error scraping URL: {url}. Error: {e}")

# Function to scrape data from the third URL
def scrape_third_url(url):
    try:
        response = requests.get("https://www.scrapethissite.com/pages/simple/")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            countries = soup.find_all('div', class_='col-md-4 country')
            data = []
            for country in countries:
                name = country.find('h3', class_='country-name').text.strip()
                capital = country.find('span', class_='country-capital').text.strip()
                population = country.find('span', class_='country-population').text.strip()
                area = country.find('span', class_='country-area').text.strip()
                data.append({
                    'name': name,
                    'capital': capital,
                    'population': population,
                    'area': area
                })
            return data
        else:
            logging.error(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error scraping URL: {url}. Error: {e}")
        return None

# Function to save data to MongoDB
def save_to_mongodb(data):
    try:
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        if isinstance(data, dict):  # Check if data is a dictionary
            # Ensure unique _id by not providing it explicitly
            if '_id' in data:
                del data['_id']
            collection.insert_one(data)
        elif isinstance(data, list):  # Check if data is a list of dictionaries
            # Ensure unique _id by not providing it explicitly
            for item in data:
                if '_id' in item:
                    del item['_id']
            collection.insert_many(data)
        client.close()
    except Exception as e:
        logging.error(f"Error saving data to MongoDB. Error: {e}")

# URLs to scrape
urls = [
    'https://www.scrapethissite.com/pages/ajax-javascript/#2015',
    'https://www.scrapethissite.com/pages/forms/',
    'https://www.scrapethissite.com/pages/advanced/'
]

# Main scraping logic
def main():
    for url in urls:
        if 'ajax-javascript' in url:
            data = scrape_main_url(url)
        elif 'forms' in url:
            data = scrape_second_url(url)
        elif 'advanced' in url:
            data = scrape_third_url(url)
        if data:
            save_to_mongodb(data)
        else:
            logging.error(f"No data scraped from URL: {url}")

if __name__ == "__main__":
    main()

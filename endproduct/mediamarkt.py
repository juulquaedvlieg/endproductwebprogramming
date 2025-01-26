import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mediamarkt(base_url, pages):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    products = []
    
    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for product in soup.find_all('p', {'data-test': 'product-title'}):
            title = product.text.strip()
            price_container = product.find_next('span', class_='sc-e0c7d9f7-0 bPkjPs')
            price = price_container.text.strip() if price_container else 'N.v.t.'
            try:
                price = float(price.replace('€', '').replace(',', '.').strip())
            except ValueError:
                price = None
            
            review_container = product.find_next('span', {'data-test': 'mms-customer-rating-count'})
            reviews = int(review_container.text.strip()) if review_container else 0
            
            rating_container = product.find_parent().find_next('div', class_='sc-56339376-2 bxZpWc')
            if rating_container:
                full_stars = len(rating_container.find_all('div', {'data-test': 'mms-fully-rated-star'}))
                partial_star = len(rating_container.find_all('div', {'data-test': 'mms-partial-rated-star'}))
                rating = full_stars + (0.5 if partial_star > 0 else 0)
            else:
                rating = 0
            
            products.append({
                'Merk': title.split()[0] if title else 'Onbekend',
                'Titel': title,
                'Prijs': price,
                'Aantal Reviews': reviews,
                'Gemiddelde Beoordeling': rating
            })
    
    return pd.DataFrame(products)

def get_data(base_url, pages):
    return scrape_mediamarkt(base_url, pages)

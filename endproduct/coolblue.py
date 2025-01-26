import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_coolblue(base_url, pages):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    items = []
    
    for page in range(1, pages + 1):
        url = f"{base_url}?pagina={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all("div", class_="product-card__title")
        
        for product in products:
            title_tag = product.find("a", class_="link")
            if not title_tag or not title_tag.text.strip():
                continue
            
            title = title_tag.text.strip()
            price_tag = product.find_next("strong", class_="sales-price__current js-sales-price-current")
            price = price_tag.text.strip().replace("€", "").replace(",", "").replace("-", "").strip() if price_tag else "Onbekend"
            
            try:
                price = float(price)
            except ValueError:
                price = None
            
            review_count_tag = product.find_next("span", class_="review-rating__reviews text--truncate")
            reviews = int(review_count_tag.text.strip().split()[0]) if review_count_tag else 0
            
            rating_tag = product.find_next("div", class_="review-stars")
            if rating_tag:
                filled_stars = len(rating_tag.find_all("svg", class_="icon--color-green"))
                grey_stars = len(rating_tag.find_all("svg", class_="icon--color-grey"))
                rating = filled_stars + (0.5 if grey_stars else 0)
            else:
                rating = 0
            
            items.append({
                'Merk': title.split()[0] if title else 'Onbekend',
                'Titel': title,
                'Prijs': price,
                'Aantal Reviews': reviews,
                'Gemiddelde Beoordeling': rating
            })
    
    return pd.DataFrame(items)

def get_data(base_url, pages):
    return scrape_coolblue(base_url, pages)

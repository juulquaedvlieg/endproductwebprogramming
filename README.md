# endproductwebprogramming
Webscraper and Dashboard for MediaMarkt and Coolblue

Here is the **README.md** translated into English:  

 Electronics Dashboard Web Scraper**  

This **Streamlit app** collects and compares electronics products from **Coolblue** and **MediaMarkt** using web scraping. The application provides insights into prices, brands, and reviews, allowing users to filter, analyze, and download data.  

---

Features

✅ Scrape** electronics product data from Coolblue and MediaMarkt 
✅ Filtering options for brand comparisons  
✅ Interactive charts for brand distribution, prices, and ratings  
✅ Comparison mode to analyze products from Coolblue and MediaMarkt  
✅ Download function to export scraped data as a CSV file  

---

🛠 Installation & Usage

1. Clone this repository: 
   ```bash
   git clone https://github.com/your-username/electronics-dashboard.git
   cd electronics-dashboard
   ```

2. Install required packages:  
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:  
   ```bash
   streamlit run app.py
   ```

---

📌 Required Packages 

This application uses the following Python libraries:  
- `streamlit` – For the interactive web interface  
- `pandas` – For data processing  
- `plotly` – For data visualization  
- `requests` & `BeautifulSoup` – For web scraping from Coolblue and MediaMarkt  

Install them with:  
```bash
pip install streamlit pandas plotly requests beautifulsoup4
```

---

🖥 How It Works  

1. Start the application and select a view 
- Coolblue: Scrape and analyze products from Coolblue  
- MediaMarkt: Scrape and analyze products from MediaMarkt  
- Comparison: Compare products from both retailers  

2. Enter the URL and page range
- Provide a category URL from Coolblue or MediaMarkt  
- Select how many pages you want to scrape  

3. View and filter the data  
- Filter by specific brands  
- Display scraped data in an interactive table  

4. Analyze data with charts**  
📌 Brand distribution
💰 Average price per brand  
Ratings per source 
💸 Price vs. rating  

5. Download data as a CSV file 

---

🔍 How Does the Web Scraper Work? 

The application uses **two separate Python scripts** for data scraping:  

1. Coolblue Scraper (`coolblue.py`)  
📥 Scrapes laptops and other electronics from Coolblue 
✅ Extracts product information, including brand, price, number of reviews, and rating  
✅ Supports multiple pages with dynamic URL handling  

Example usage in code: 
```python
import coolblue

df = coolblue.get_data("https://www.coolblue.nl/laptops", 3)
print(df.head())
```

---

2. MediaMarkt Scraper (`mediamarkt.py`) 
📥 Scrapes laptops and other electronics from MediaMarkt 
✅ Extracts product information, including price, rating, and number of reviews  
✅ Supports multiple pages with dynamic pagination  

Example usage in code:  
```python
import mediamarkt

df = mediamarkt.get_data("https://www.mediamarkt.nl/nl/category/laptops", 3)
print(df.head())
```

---

Important Notes**  

- Ensure that you use the correct category URLs from Coolblue and MediaMarkt.  
- The scraper will work as long as the website structure remains unchanged. If issues arise, check for site updates.  
- This tool is intended for personal use only, and you should respect the **robots.txt** rules of the websites you scrape.  

---

Future Improvements  

🔹 Improve the user interface and design  
🔹 Add support for more e-commerce platforms  
🔹 Extend with advanced analytical features  

---

📌 Author: Your Name  
📂 Repository: [GitHub](https://github.com/your-username/electronics-dashboard)  

🚀 Enjoy your data analysis and price comparisons!  

---

Would you like to add extra details, such as screenshots or a demo? Let me know! 😊

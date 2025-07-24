import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_flipkart(search_query, num_pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    products = []

    for page in range(1, num_pages + 1):
        url = f"https://www.flipkart.com/search?q={search_query}&page={page}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.find_all("div", class_="_1AtVbE")  # Flipkart uses nested containers

        for item in items:
            name = item.find("div", class_="_4rR01T")
            price = item.find("div", class_="_30jeq3")
            rating = item.find("div", class_="_3LWZlK")

            if name and price:
                products.append({
                    "Product Name": name.text.strip(),
                    "Price": price.text.strip(),
                    "Rating": rating.text.strip() if rating else "N/A"
                })

    return products

# Run the scraper
if __name__ == "__main__":
    search_term = "iphone"
    data = scrape_flipkart(search_term, num_pages=2)

    df = pd.DataFrame(data)
    df.to_csv("flipkart_results.csv", index=False)
    print(f"Scraped {len(df)} products and saved to flipkart_results.csv")

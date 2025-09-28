import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape products
def scrape_products(search_query):
    url = f"https://www.flipkart.com/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_names = []
    product_prices = []
    product_ratings = []

    # Each product card container
    products = soup.find_all('div', {'class': '_1AtVbE'})

    for product in products:
        name_tag = product.find('div', {'class': '_4rR01T'})
        price_tag = product.find('div', {'class': '_30jeq3 _1_WHN1'})
        rating_tag = product.find('div', {'class': '_3LWZlK'})

        if name_tag and price_tag:
            product_names.append(name_tag.text)
            product_prices.append(price_tag.text)
            product_ratings.append(rating_tag.text if rating_tag else "No Rating")

    # Save to CSV
    df = pd.DataFrame({
        'Product Name': product_names,
        'Price': product_prices,
        'Rating': product_ratings
    })

    filename = f"{search_query}_products.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Example usage
search_keyword = input("Enter the product keyword: ")
scrape_products(search_keyword)

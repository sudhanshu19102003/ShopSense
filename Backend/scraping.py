import requests
from bs4 import BeautifulSoup

def get_amazon_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Scrape product title
        product_title = soup.select_one("span#productTitle")
        if product_title:
            product_title = product_title.get_text().strip()

        # Scrape "About this item" section
        about_section = soup.select_one("div#feature-bullets ul")
        if about_section:
            about_text = "\n".join([item.get_text().strip() for item in about_section.find_all("li")])

        # Scrape top 10 comments
        top_10_comments = soup.select("div[data-hook='review-collapsed']")
        top_10_comments = [comment.get_text().strip() for comment in top_10_comments[:10]]

        return {
            "product_title": product_title,
            "about_section": about_text,
            "top_10_comments": top_10_comments
        }
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None
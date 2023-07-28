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
        
        #Scrape product version selection
        product_v = soup.select('div.a-section table tr')
        if product_v:
            for row in product_v:
                cells = row.select('td')
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    product_v[key] = value

        # Scrape "About this item" section
        about_section = soup.select_one("div#feature-bullets ul")
        if about_section:
            about_text = "\n".join([item.get_text().strip() for item in about_section.find_all("li")])

        # Scrape top comments
        top_comments = soup.select("div[data-hook='review-collapsed']")
        top_comments = [comment.get_text().strip() for comment in top_comments[:50]]

        return {
            "product_title": product_title,
            "product_title": product_v,
            "about_section": about_text,
            "top_comments": top_comments
        }
    
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None
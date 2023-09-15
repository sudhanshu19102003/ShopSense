import requests
from bs4 import BeautifulSoup
import title
from urllib.parse import urlparse, urlunparse



def get_amazon_product_data(url):
    url=shorten_amazon_url(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Scrape product title(1)
        product_title = soup.select_one("span#productTitle")
        if product_title:
            product_title = title.generate_title(product_title.get_text())
        
        #Scrape product version selection(2)
        product_v = {}
        product_v_rows = soup.select('div.a-section table tr')
        if product_v_rows:
            for row in product_v_rows:
                cells = row.select('td')
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    product_v[key] = value
        else:
            print("no_product version")

                   
        #Scrape Technical Details:(3)
        Technical_Details={}
        Technical_Details_table = soup.find("table", {"id": "productDetails_techSpec_section_1"})
        if Technical_Details_table:
            rows = Technical_Details_table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                Technical_Details[key] = value
                Technical_Details[key] = Technical_Details[key].replace('\u200e', '')
        else:
            print("no_Technical_Details")            


        # Scrape "About this item" section(4)
        about_section = soup.select_one("div#feature-bullets ul")
        if about_section:
            about_text = "\n".join([item.get_text().strip() for item in about_section.find_all("li")])
        else:
            about_text=""
            print("no_about_text")

        # Scrape top comments(5)
        top_comments = soup.select("div[data-hook='review-collapsed']")
        if top_comments:
            top_comments = [comment.get_text().strip() for comment in top_comments[:10]]
        else:
            print("no_top_comments")
        
        # Find the div element with id="productDescription"(6)
        product_description_div = soup.find('div', id='productDescription')

        product_description = None
        if product_description_div:
            product_description = product_description_div.text
        else:
            print("no_product_description")

        return {
            "product_title": product_title,
            "product_V": product_v,
            "about_section": about_text,
            "technical_details": Technical_Details,
            "top_comments": top_comments,
            "product_description": product_description
        }
    
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None
    
def shorten_amazon_url(original_url):
    parsed_url = urlparse(original_url)
    path_segments = parsed_url.path.split('/')
    shortened_path = '/'.join(path_segments[:4])  # Keep the first 4 path segments
    return urlunparse((parsed_url.scheme, parsed_url.netloc, shortened_path, '', '', ''))

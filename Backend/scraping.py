import requests
from bs4 import BeautifulSoup
import title


def get_amazon_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
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
            
            #Printing Technical_Details to determine whether issue #1 has been successfully fixed
            print("Technical_Details:",Technical_Details)


        # Scrape "About this item" section(4)
        about_section = soup.select_one("div#feature-bullets ul")
        if about_section:
            about_text = "\n".join([item.get_text().strip() for item in about_section.find_all("li")])
        else:
            about_text=""

        # Scrape top comments(5)
        top_comments = soup.select("div[data-hook='review-collapsed']")
        top_comments = [comment.get_text().strip() for comment in top_comments[:50]]

        return {
            "product_title": product_title,
            "product_V": product_v,
            "about_section": about_text,
            "technical_details": Technical_Details,
            "top_comments": top_comments
        }
    
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None

import requests
from bs4 import BeautifulSoup
from llm import generate_title,summarizer,chat
from comment_analyzer import predict_average_rating



def process_html_content(page):
    soup = BeautifulSoup(page, "html.parser")
    
    # Scrape product title(1)
    product_title = soup.select_one("span#productTitle")
    if product_title:
        product_title = product_title.get_text(strip=True)
        r=1
    else:
        r=0
    
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
    # Scrape ratings
    ratings = soup.select("i[data-hook='review-star-rating'] span.a-icon-alt")
    if ratings:
        ratings = [int(rating.get_text().strip()[0]) for rating in ratings[:10]]
    else:
        print("no_ratings")
    if ratings and top_comments:
        formated_rating = []
        for comment, rating in zip(top_comments, ratings):
            formated_rating.append([comment, rating])

    
    # Find the div element with id="productDescription"(6)
    product_description_div = soup.find('div', id='productDescription')
    product_description = None
    if product_description_div:
        product_description = product_description_div.get_text(strip=True)
    else:
        print("no_product_description")
    llm_data={
        "product_title": product_title,
        "about_section": about_text,
        "product_description": product_description
    }
    chat_data={
        "product_title": product_title,
        "product_V": product_v,
        "about_section": about_text,
        "technical_details": Technical_Details,
        "product_description": product_description
    }
    output={
        "product_title": generate_title(product_title),
        "top_comments": str(predict_average_rating(formated_rating)),
        "product_description": summarizer(llm_data),
        "data": chat_data
    }
    print(output)
    return output,r
    
def chat_answer(data):
    return chat(data)

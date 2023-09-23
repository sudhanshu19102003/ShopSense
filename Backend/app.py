from flask import Flask, request, jsonify
import requests
import scraping

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_website():
    data = request.get_json()

    if 'website_link' not in data:
        return jsonify({'error': 'Missing website_link in the request body'}), 400

    website_link = data['website_link']

    try:
       
        output = scraping.get_amazon_product_data(website_link)
        print(type(output["top_comments"]))
        print(len(output["top_comments"]))

        return jsonify(output), 200

    except requests.exceptions.MissingSchema:
        return jsonify({'error': 'Invalid website link provided'}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

def model():
    """"""
    pass   

if __name__ == '__main__':
    app.run(debug=True)
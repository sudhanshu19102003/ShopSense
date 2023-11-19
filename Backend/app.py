from flask import Flask, request, jsonify
import requests
from json import dumps
from scraping import get_amazon_product_data,chat_answer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

@app.route('/scrape', methods=['POST'])
def scrape_website():
    data = request.get_json()

    if 'website_link' not in data:
        return jsonify({'error': 'Missing website_link in the request body'}), 400

    website_link = data['website_link']

    try:
       
        output = get_amazon_product_data(website_link)
        print(output)
        return jsonify(output), 200

    except requests.exceptions.MissingSchema:
        return jsonify({'error': 'Invalid website link provided'}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    

@app.route('/chat', methods=['POST'])
def chat_answers():
    try:
        data = request.get_json()
        print(data)
        response = chat_answer(data)
        response_json = {'response': response}
        return jsonify(response_json), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error in /chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
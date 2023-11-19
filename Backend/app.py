from flask import Flask, request, jsonify
import sqlite3
from scraping import process_html_content,chat_answer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app
import os

@app.route('/scrape', methods=['POST'])
def scrape_website():
    data = request.get_json()

    if 'website_html' not in data:
        return jsonify({'error': 'Missing website_html in the request body'}), 400

    website_html = data['website_html']
    #print(website_html)
    try:
        # Process the HTML content and extract the data
        output,key = process_html_content(website_html)
        return jsonify(output), 200

    except Exception as e:
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
import requests
import json

def analyze_reviews_and_get_average(reviews):
    model_url=""
    try:
        # Create a request payload
        payload = {"inputs": reviews}

        # Send a POST request to TensorFlow Serving
        response = requests.post(model_url, json=payload)

        # Parse the response
        result = json.loads(response.text)
        predictions = result['predictions']

        # Calculate the average of the predictions
        average_prediction = sum(predictions) / len(predictions)

        return average_prediction

    except Exception as e:
        # Handle errors gracefully
        print(f"An error occurred: {str(e)}")
        return None

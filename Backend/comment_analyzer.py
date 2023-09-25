from tensorflow import keras
import tensorflow_text
import pandas as pd
import numpy as np

model = keras.models.load_model("Backend/model")


def predict_average_rating(formatted_result):
    text_data = [item[0] for item in formatted_result]
    rating_data = [item[1] for item in formatted_result]

    text_data = np.array(text_data)
    rating_data = np.array(rating_data)

    # Make predictions using the model
    predictions = model.predict([text_data, rating_data])

    # Calculate the average prediction
    average_prediction = round(np.mean(predictions)*5, 1)
    print("\n go \n" )
    print(average_prediction)

    return average_prediction
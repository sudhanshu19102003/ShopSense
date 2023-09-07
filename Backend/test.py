import tensorflow as tf

# Define the path to the saved model directory
model_directory = 'model V2'

# Load the saved model
loaded_model = tf.keras.models.load_model(model_directory)

# Print model summary
loaded_model.summary()
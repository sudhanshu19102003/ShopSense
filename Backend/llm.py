from transformers import T5Tokenizer, T5ForConditionalGeneration
from tensorflow import keras
import tensorflow_text as tf_text

loaded_model = keras.models.load_model("Backend/model")
if loaded_model:
    print("\n loaded model \n")

# Load the pre-trained model and tokenizer
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
model.to("cuda")  # Move the model to the GPU if available

def answer(question, context, max_length):
    # Split the context into smaller chunks to fit within the model's maximum sequence length
    max_seq_length = 512  # Maximum sequence length supported by the model
    chunks = [context[i:i+max_seq_length] for i in range(0, len(context), max_seq_length)]

    # Initialize an empty answer
    combined_answer = ""

    for chunk in chunks:
        # Combine the question and chunk of context
        input_text = f"{question}: {chunk}\n Solution: "
        print(input_text)

        # Tokenize and generate the answer for this chunk
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
        outputs = model.generate(input_ids, max_length=max_length)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Append the answer for this chunk to the combined answer
        combined_answer += answer

    return combined_answer

def generate_title(data):
    question = """For crafting shorter, generic product titles, start with a simple descriptor that captures the product's purpose, followed by the brand name or identifier and any crucial specifications. Strive for brevity and clarity to make the title easily applicable to various products. \n
    
    Example 1: Crucial RAM 8GB DDR4 3200MHz CL22 (or 2933MHz or 2666MHz) Laptop Memory CT8G4SFRA32A
    Solution: Memory Upgrade: Crucial 8GB DDR4 Laptop RAM

    Example 2: V-Guard Divino 5 Star Rated 15 Litre Storage Water Heater (Geyser) with Advanced 4 Level Safety, White.
    Solution: V-Guard Divino 15L 5-Star Water Heater

    Example 3: Convenient Gym Shaker Bottle: Boldfit Compact 500ml
    Solution: Boldfit Compact 500ml Gym Shaker Bottle

    Example 4

    """
    return answer(question, data, 15)

def format_for_llm(product_info):
    prompt = "this is the product information"
    for key, value in product_info.items():
        if value is not None:
            prompt += f"{key.replace('_', ' ')}: {value}\n"
    return prompt

def summarizer(data):
    question = "Explain about the product in short with the importent points"
    data=format_for_llm(data)
    return answer(question, data, 350)



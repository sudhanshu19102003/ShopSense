from transformers import T5Tokenizer, T5ForConditionalGeneration

def generate_product_title(question, context):
    # Load the pre-trained model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
    model.to("cuda")  # Move the model to the GPU if available

    # Combine the question and context
    input_text = f"question: {question}\n{context}"

    # Tokenize and generate the answer
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")

    outputs = model.generate(input_ids)
    answer = tokenizer.decode(outputs[0])

    return answer
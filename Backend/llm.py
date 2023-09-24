from transformers import T5Tokenizer, T5ForConditionalGeneration

def answer(question, context, max_length):
    # Load the pre-trained model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
    model.to("cuda")  # Move the model to the GPU if available

    # Split the context into smaller chunks to fit within the model's maximum sequence length
    max_seq_length = 512  # Maximum sequence length supported by the model
    chunks = [context[i:i+max_seq_length] for i in range(0, len(context), max_seq_length)]

    # Initialize an empty answer
    combined_answer = ""

    for chunk in chunks:
        # Combine the question and chunk of context
        input_text = f"question: {chunk}\n{question}"

        # Tokenize and generate the answer for this chunk
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
        outputs = model.generate(input_ids, max_length=max_length)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Append the answer for this chunk to the combined answer
        combined_answer += answer

    return combined_answer

def generate_title(data):
    question = "give an title"
    data=format_for_llm(data)
    return answer(question, data, 10)

def format_for_llm(product_info):
    prompt = ""
    for key, value in product_info.items():
        if value is not None:
            prompt += f"{key.replace('_', ' ').title()}: {value}\n"
    return prompt

def summarizer(data):
    question = "summarizer"
    data=format_for_llm(data)
    return answer(question, data, 450)



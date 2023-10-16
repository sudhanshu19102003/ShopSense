from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the pre-trained model and tokenizer
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
model.to("cuda")  # Move the model to the GPU if available

def answer(question, context, max_length, min):
    if question or context is not None:
        # Split the context into smaller chunks to fit within the model's maximum sequence length
        max_seq_length = 512  # Maximum sequence length supported by the model
        chunks = [context[i:i+max_seq_length] for i in range(0, len(context), max_seq_length)]
    
        # Initialize an empty answer
        combined_answer = ""
    
        for chunk in chunks:
            # Combine the question and chunk of context
            input_text = f"{question}: \ncontext:{str(chunk)}\nSolution:"
            #print(input_text)
    
            # Tokenize and generate the answer for this chunk
            input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
            outputs = model.generate(input_ids, max_length=max_length, min_length=min)
            answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Append the answer for this chunk to the combined answer
            combined_answer += answer
            #combined_answer=answer("structure to answer properly:", combined_answer, max_length, min)
        
        return combined_answer

def generate_title(data):
    question = """For crafting shorter, generic product titles, start with a simple descriptor that captures the product's purpose, followed by the brand name or identifier and any crucial specifications. Strive for brevity and clarity to make the title easily applicable to various products. \n
    
    Example 1:
    context: Crucial RAM 8GB DDR4 3200MHz CL22 (or 2933MHz or 2666MHz) Laptop Memory CT8G4SFRA32A
    Solution: Memory Upgrade: Crucial 8GB DDR4 Laptop RAM

    Example 2: 
    context: V-Guard Divino 5 Star Rated 15 Litre Storage Water Heater (Geyser) with Advanced 4 Level Safety, White.
    Solution: V-Guard Divino 15L 5-Star Water Heater

    Example 3:
    context: Convenient Gym Shaker Bottle: Boldfit Compact 500ml
    Solution: Boldfit Compact 500ml Gym Shaker Bottle

    Example 4

    """
    if data is not None:
        return answer(question, data, 15,1)

def format_for_llm(product_info):
    prompt = "this is the product information"
    for key, value in product_info.items():
        if value is not None:
            prompt += f"{key.replace('_', ' ')}: {value}\n"
    return prompt

def summarizer(data):
    if data is not None:
        question = "Explain about the product in short with the importent points"
        data=format_for_llm(data)
        return answer(question, data, 1000,1)

def chat(data):
    if data is not None:
        question = f"""Answer the question based on the context below. Keep the answer short. Respond "Unsure about answer" if not sure about the answer. \n
                    Question: {data.get("question")}"""
        context = format_for_llm(data.get("context"))
        output=answer(context,question,50,3)
        return output

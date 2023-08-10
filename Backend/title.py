from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import pickle
nltk.download('punkt')

def generate_title(inputs):
    print(inputs)
    tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-small-medium-title-generation")
    model = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-small-medium-title-generation")
    
    inputs = tokenizer(inputs, max_length=1026, truncation=True, return_tensors="pt")
    output = model.generate(**inputs, num_beams=8, do_sample=True, min_length=2, max_length=10)
    decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]

    return predicted_title

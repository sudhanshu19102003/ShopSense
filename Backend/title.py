from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import pickle
nltk.download('punkt')

def generate_title(max_input_length=1024):
    with open('promts/promt.pkl', 'rb') as pkl_file:
        input_text = pickle.load(pkl_file)
    print(input_text)
    tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-small-medium-title-generation")
    model = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-small-medium-title-generation")

    inputs = ["summarize: " + input_text]

    inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, return_tensors="pt")
    output = model.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=64)
    decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]

    return predicted_title

text = """7 feet Lightweight & Portable (84 Inch) Long Tripod Stand for YouTube | Photo-Shoot | Video Shoot | Live Stream | Makeup | 360-degree Rotation for All Mobiles & Cameras"""
predicted_title = generate_title(text)
print(predicted_title)

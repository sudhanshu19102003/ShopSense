# this should have an funtion which has the input lookes like this [comment0,comment1,.,...]
#some usefull links https://huggingface.co/Sarwar242/autotrain-fake-reviews-labelling-37433101195
#the funtion must output an graph in html
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

class model():
    def __init__(self):       
        """
        Model setup
        
        """
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained("./model")
        except:
            print("Downloading model...")
            os.system("git clone https://huggingface.co/Sarwar242/autotrain-fake-reviews-labelling-37433101195")
            os.rename("autotrain-fake-reviews-labelling-37433101195", "model")
            self.model = AutoModelForSequenceClassification.from_pretrained("./model")

        self.tokenizer = AutoTokenizer.from_pretrained("./model")

    def tokenize(self, text):
        return self.tokenizer(text, return_tensors="pt")

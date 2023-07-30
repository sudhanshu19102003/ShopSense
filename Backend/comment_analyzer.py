# this should have an funtion which has the input lookes like this [comment0,comment1,.,...]
#some usefull links https://huggingface.co/Sarwar242/autotrain-fake-reviews-labelling-37433101195
#the funtion must output an graph in html
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

class model():
    def __init__(self):       
        pass
    
    def setup(self,hf_repo:str):
        """
        It sets up HF model

        It downloads the model repo from HF and saves it and rename it as ./model in the current directory.

        Args:
                hf_repo (str): HF repo name

        Returns:
                None
        
        """
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained("./model")
        except:
            print("Error model not found.")
            print("Downloading model...")
            os.system("git clone https://huggingface.co/", hf_repo)
            hf_repo = hf_repo.split("/")[1]
            os.rename(hf_repo, "model")
            self.model = AutoModelForSequenceClassification.from_pretrained("./model")


        self.tokenizer = AutoTokenizer.from_pretrained("./model")
        return None

    def tokenize(self, text:str):
        """
        It tokenizes the text
        
        It takes top_comments from scrape_website() and tokenizes them.

        Args:
                text (str): text to be tokenized

        Returns:
                dict: tokenized text
        
        """
        return self.tokenizer(text, return_tensors="pt")
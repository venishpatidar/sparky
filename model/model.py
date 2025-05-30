import torch
from config import config
from transformers import T5Tokenizer, T5ForConditionalGeneration


class SparkyNPL2JSON:
    """
        Extracts the information from Natural language strig 
        to JSON object.
    """
    def __init__(self,model_path:str="") -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = T5Tokenizer.from_pretrained(
            model_path or config.MOEDL_PATH
        )
        self.model = T5ForConditionalGeneration.from_pretrained(
            config.MOEDL_PATH or config.MOEDL_PATH
        )
        self.model.to(self.device)

    def _tokenize(self,input):
        return self.tokenizer(
                input,
                truncation=True,
                padding="max_length",
                max_length=256,
                return_tensors="pt"
            ).to(self.device)

    def generate(self,text:str)->dict:
        """
            uses the pretrained model to 
            predict the translated sequence
            and return the dict of extracted
            information
        """
        input = self._tokenize(text)
        with torch.no_grad():
            output = self.model.generate(**input,max_length=256)
        decoded_output = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return self.__convert_to_json(decoded_output)

    def __convert_to_json(self,text:str)->dict:
        """
            Helper function to convert the 
            generated text to JSON,
            the function is hardcoded to expect some 
            white space and can breakdown at somepoint  
        """
        return {key: (None if value == 'null' else value) for t in text.replace(": ", ":").split(", ") for key, value in [t.split(":")]}


if __name__=="__main__":
    model = SparkyNPL2JSON()
    text="What is the course code for Sustainable Civil and Environmental Systems Engineering?"
    print(model.generate(text))
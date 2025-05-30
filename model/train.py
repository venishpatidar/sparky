from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import TrainingArguments, Trainer # type: ignore
from datasets import Dataset
from torch.utils.data import random_split
import json
import torch
import utils
from config import config


DATASET_PATH = './dataset/dataset.json'

class T5Trainer:
    def __init__(self, model_name="", dataset_path=DATASET_PATH):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.tokenizer = T5Tokenizer.from_pretrained(config.MODEL_PATH)
        self.model = T5ForConditionalGeneration.from_pretrained(config.MODEL_PATH).to(self.device) # type: ignore

        # Load and preprocess dataset
        self.dataset = self._create_dataset(dataset_path)

        # Spliting Dataset 80%-20%
        train_size = int(0.8 * len(self.dataset))
        val_size = len(self.dataset) - train_size
        self.train_dataset, self.val_dataset = random_split(self.dataset, [train_size, val_size])#type: ignore
        

    def _tokenize(self,input):
        return self.tokenizer(
                input,
                truncation=True,
                padding="max_length",
                max_length=256,
                return_tensors="pt"
            ).to(self.device)


    def _load_dataset(self, path):
        """
        Loads the dataset from a given JSON file path.

        Expects the file to contain a list of dictionaries with the structure:
        {
            "prompt": "...",
            "responses": "..."
        }

        Args:
            path (str): Path to the dataset JSON file.

        Returns:
            list: A list of dictionaries with prompt-response pairs.
        """
        data = []
        with open(path, 'r') as file:
            data = json.load(file)
        return data


    def _preprocess(self, data):
        """
        Preprocesses the raw data using a utility function that tokenizes
        the prompt and response fields for each entry.

        Args:
            data (list): List of dictionaries containing raw text data.

        Returns:
            list: List of tokenized input-output pairs.
        """
        return [utils.tokenize_data(data_point, self._tokenize) for data_point in data]

    def _create_dataset(self, dataset_path):
        """
        Loads and preprocesses the dataset, then converts it into a Hugging Face
        `Dataset` object for model training or evaluation.

        Args:
            dataset_path (str): Path to the JSON dataset file.

        Returns:
            Dataset: A Hugging Face Dataset object with input_ids, attention_mask, and labels.
        """
        tokenized_dataset = self._preprocess(self._load_dataset(dataset_path))
        return Dataset.from_dict({
            'input_ids': [data_point['input_ids'].squeeze() for data_point in tokenized_dataset],
            'attention_mask': [data_point['attention_mask'].squeeze() for data_point in tokenized_dataset],
            'labels': [data_point['labels'].squeeze() for data_point in tokenized_dataset],
        })



    def train(self,num_train_epochs=1,output_dir="./T5-finetuned-sparky",learning_rate=2e-5,batch_size=8):
        # Training arguments
        args = TrainingArguments(
            output_dir=output_dir,
            save_strategy = "no", # can be "epoch" and that will save weight after each epoch
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_train_epochs,
            weight_decay=0.01,
            # logging_dir="./logs",
            # logging_steps=10,
        )

        trainer = Trainer(
            model=self.model,
            args=args,
            train_dataset=self.train_dataset,
            eval_dataset=self.val_dataset,  # Replace with split if needed
            processing_class=self.tokenizer,
        )
        trainer.train()

    def infer(self, text: str):
        self.model.eval()
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=256
        ).to(self.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_length=256)
            return self.tokenizer.decode(output[0], skip_special_tokens=True)

if __name__ == "__main__":
    trainer = T5Trainer()
    
    # Start Training
    trainer.train()
    
    # Sample inference
    test_query = "Can you tell me the course number for Cross-Cultural Communication and Negotiation in AME?"
    response = trainer.infer(test_query)
    print("Sample Output:", response)


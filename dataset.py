from collections import defaultdict
import os
import json
import random
from dataset.question_templates import question_templates

DATASET_DIR = "dataset"
DATASET_COMBINATION_FILE_NAME = "dataset_componenets.json"
DATASET_FILE = "dataset.json"

class DatasetProcessor:

    def __init__(self) -> None:
        self.question_templates = question_templates
        self.dataset_parameters = {}
        self.conversational_data = []

    def get_dataset_parameters(self, folder_path:str=DATASET_DIR, file_name:str=DATASET_COMBINATION_FILE_NAME)->None:
        """
        Expects the dataset of the form:
            {
                course_stack:  [],
                course_number: [],
                course_name:   [],
                course_code:   [],
            }
        """
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.dataset_parameters = json.load(file)
        else:
            print(f"[x] Error: {folder_path}/{file_name} doesnot exist.")

    def generate_conversational_data(self,num_iteration:int=100)->None:
        """
            Itreate over the question templates and 
            generates the conversational training data,
            by randomly selecting the arguments from the 
            databse.
        """
        for i in range(num_iteration):
            course_stack = random.choice(self.dataset_parameters['course_stack']) 
            course_number = random.choice(self.dataset_parameters['course_number']) 
            course_name = random.choice(self.dataset_parameters['course_name']) 
            course_code = random.choice(self.dataset_parameters['course_code']) 
            faculty_name = random.choice(self.dataset_parameters['faculty_name'])
            
            for question in self.question_templates:
                self.conversational_data.append({
                    "prompt": question.format(
                        course_stack=course_stack,
                        course_number=course_number,
                        course_name=course_name,
                        course_code=course_code,
                        faculty_name=faculty_name
                    ),
                    "response": {
                        "course_stack": course_stack if "course_stack" in question else None,
                        "course_number": course_number if "course_number" in question else None,
                        "course_name": course_name if "course_name" in question else None,
                        "course_code": course_code if "course_code" in question else None,
                        "faculty_name": faculty_name if "faculty_name" in question else None,
                    }
                })
            print(f"{i+1}/{num_iteration} iteration done.")

    def export_dataset(self, folder_path:str=DATASET_DIR, file_name:str=DATASET_FILE) -> None:
        """
            Export the data in json format
        """
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as json_file:
            json.dump(self.conversational_data, json_file, indent=2)
        print(f"Conversational data exported sucessfully")


if __name__ == "__main__":
    dp = DatasetProcessor()
    dp.get_dataset_parameters()
    dp.generate_conversational_data()
    dp.export_dataset()

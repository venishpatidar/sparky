from collections import defaultdict
import os
import json

DATASET_PATH = "dataset"
DATASET_COMBINATION_FILE_NAME = "dataset_combination.json"
DATASET_FILE = "dataset.json"

class DatasetProcessor:

    def __init__(self) -> None:
        self.question_templates = defaultdict(list)
        self.dataset_parameters = []
        self.conversational_data = []


    def get_question_templates(self)->None:
        self.question_templates = {
            "course_stack": [
                    "What is the full form of {}?",
                    "Which program stack is referred to as {}?",
                    "What department does the stack {} represent?",
                    "What is the abbreviation for the {} stack?",
                    "Can you tell me what {} stands for?",
                    "What is the program name for stack {}?",
                    "In which department does the {} stack belong?",
                    "Which program category is represented by {}?",
                    "Can you provide more information on the {} stack?",
                    "What is the meaning of the abbreviation {}?"
                ],
                "course_number": [
                    "What is the course number for {}?",
                    "Which course is represented by the number {}?",
                    "What is the number assigned to {}?",
                    "Can you give me the course number for {}?",
                    "Which course number is associated with {}?",
                    "Which course comes with the number {}?",
                    "Can you tell me the number of the course titled {}?",
                    "What number identifies the course {}?",
                    "Can you provide the course number for {}?",
                    "What is the course code number for the class {}?"
                ],
                "course_name": [
                    "What is the name of the course with code {}?",
                    "Can you tell me the course name for {}?",
                    "What is the title of the course under code {}?",
                    "What is the name of the course with number {}?",
                    "What is the course title for {}?",
                    "Which course is identified by the code {}?",
                    "What course does the number {} refer to?",
                    "Can you tell me what course is numbered {}?",
                    "What is the name of the course that has code {}?",
                    "Which course is associated with the code {}?"
                ],
                "course_code": [
                    "What is the course code for {}?",
                    "What is the code used for enrolling in {}?",
                    "Can you provide the registration code for {}?",
                    "What is the identifier code for {}?",
                    "Which code is used for registering in {}?",
                    "Can you tell me the course code for {}?",
                    "What is the unique code for the course {}?",
                    "Which registration code applies to {}?",
                    "What code do I need to register for {}?",
                    "What is the identifier number for the course titled {}?"
                ],
                "faculty_name": [
                    "Who is the instructor for {}?",
                    "Who teaches the course {}?",
                    "Can you tell me who the faculty is for {}?",
                    "Who is the professor of {}?",
                    "Which professor teaches {}?",
                    "Can you provide the name of the instructor for {}?",
                    "Who is responsible for teaching {}?",
                    "Who is assigned to the course titled {}?",
                    "Can you tell me the faculty member for course code {}?",
                    "Who is the course instructor for {}?"
                ]
        }

    def get_dataset_parameters(self, folder_path=DATASET_PATH, file_name=DATASET_COMBINATION_FILE_NAME)->None:
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    self.dataset_parameters = json.load(file)
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")

    def generate_conversational_data(self):
        for category, template_question in self.question_templates.items():
            for courses_data in self.dataset_parameters:
                response = {
                    "course_stack": None,
                    "course_number": None,
                    "course_name": None,
                    "course_code": None,
                    "faculty_name": None
                }
                response[category] = courses_data[category]
                for question in template_question:
                    self.conversational_data.append({
                        "prompt": question.format(courses_data[category]),
                        "response": response
                    })

    def export_dataset(self, folder_path=DATASET_PATH, file_name=DATASET_FILE) -> None:

        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as json_file:
            json.dump(self.conversational_data, json_file, indent=2)






if __name__ == "__main__":
    dp = DatasetProcessor()
    dp.get_question_templates()
    dp.get_dataset_parameters()
    dp.generate_conversational_data()
    dp.export_dataset()

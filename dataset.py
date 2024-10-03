from collections import defaultdict
import os
import json
from dataset.question_templates import question_templates

DATASET_DIR = "dataset"
DATASET_COMBINATION_FILE_NAME = "dataset_componenets.json"
DATASET_FILE = "dataset.json"

class DatasetProcessor:

    def __init__(self) -> None:
        self.question_templates = question_templates
        self.dataset_parameters = []
        self.conversational_data = []

    def get_dataset_parameters(self, folder_path=DATASET_DIR, file_name=DATASET_COMBINATION_FILE_NAME)->None:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.dataset_parameters = json.load(file)
        else:
            print(f"[x] Error: {folder_path}/{file_name} doesnot exist.")

    def get_faculty_name(self, courses_data):
        if courses_data['faculty_name']:
            if len(courses_data['faculty_name']) == 1:
                return courses_data["faculty_name"][0]
            else:
                for name in courses_data["faculty_name"]:
                    if "Staff" not in name:
                        return name
        else:
            return None

    def generate_conversational_data(self):
        """
            {
                course_stack:  [],
                course_number: [],
                course_name:   [],
                course_code:   [],
            }
        """


        for courses_data in self.dataset_parameters:
            faculty_name = self.get_faculty_name(courses_data)
            for question in self.question_templates:
                prompt = question.format(
                    course_stack=courses_data["course_stack"],
                    course_number=courses_data["course_number"],
                    course_name=courses_data["course_name"],
                    course_code=courses_data["course_code"],
                    faculty_name=faculty_name
                )
                response = {
                    "course_stack": None,
                    "course_number": None,
                    "course_name": None,
                    "course_code": None,
                    "faculty_name": None
                }

                if "course_stack" in question:
                    response["course_stack"] = courses_data["course_stack"]
                if "course_number" in question:
                    response["course_number"] = courses_data["course_number"]
                if "course_name" in question:
                    response["course_name"] = courses_data["course_name"]
                if "course_code" in question:
                    response["course_code"] = courses_data["course_code"]
                if "faculty_name" in question:
                    response["faculty_name"] = faculty_name

                # Add the prompt and response to the conversation data
                self.conversational_data.append({"prompt": prompt, "response": response})

    def export_dataset(self, folder_path=DATASET_DIR, file_name=DATASET_FILE) -> None:

        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as json_file:
            json.dump(self.conversational_data, json_file, indent=2)


if __name__ == "__main__":
    dp = DatasetProcessor()
    dp.get_dataset_parameters()
    dp.generate_conversational_data()
    dp.export_dataset()

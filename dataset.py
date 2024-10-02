from collections import defaultdict
import os
import json

DATASET_PATH = "dataset"
DATASET_COMBINATION_FILE_NAME = "dataset_combination.json"
DATASET_FILE = "dataset.json"

class DatasetProcessor:

    def __init__(self) -> None:
        self.question_templates = []
        self.dataset_parameters = []
        self.conversational_data = []


    def get_question_templates(self)->None:
        self.question_templates = [
            # Questions about course stack
                "What is the full form of {course_stack}?",
                "What does {course_stack} stand for?",
                "Can you explain what {course_stack} represents in this context?",
                "Which courses fall under the {course_stack} category?",
                "Are there any courses in the {course_stack} stack I can take?",

                # Questions about course number
                "What is the course number for {course_name}?",
                "Which course has the number {course_number}?",
                "Is there a course with number {course_number} in the {course_stack} group?",
                "Can you tell me the course number for {course_name} in {course_stack}?",
                "What course is identified with the number {course_number}?",

                # Questions about course name
                "What is the name of the course with course number {course_number}?",
                "Which course is named {course_name}?",
                "Do you offer a course called {course_name} in {course_stack}?",
                "Can you tell me the name of the course with course code {course_code}?",
                "What is the course name for {course_code}?",

                # Questions about course code
                "What is the course code for {course_name}?",
                "Can you give me the code for the course {course_name}?",
                "What course has the code {course_code}?",
                "Which course is identified by the code {course_code}?",
                "What is the code for the course {course_name}?",

                # Questions about faculty name
                "Who is the instructor for {course_name}?",
                "Which faculty member teaches {course_name}?",
                "Who is responsible for teaching {course_name}?",
                "Can you tell me who teaches the course with code {course_code}?",
                "Who is the faculty member for the course {course_stack} {course_number}?",
                "Is {faculty_name} teaching any course this semester?",
                "Which courses are taught by {faculty_name}?",
                "Do you know the instructor for {course_stack} courses?",
                "Is {faculty_name} the professor for any {course_stack} courses?",

                # General enrollment-related questions
                "What courses are available under {course_stack}?",
                "Are there any faculty members teaching {course_stack} courses?",
                "What is the code for the course I need to enroll in {course_stack}?",
                "How can I find out the faculty for {course_stack} courses?",
                "Can you give me the course number for any {course_stack} courses?",
                "Can I take {course_stack} courses in this semester?",
                "Is {faculty_name} associated with {course_stack} courses this semester?",
                "How can I find the instructor for {course_name}?",
                "Which courses can I take under {course_stack} group?",
                "Is there a course in {course_stack} with the name {course_name}?",
                "Who teaches {course_stack} {course_number}?"
        ]

    def get_dataset_parameters(self, folder_path=DATASET_PATH, file_name=DATASET_COMBINATION_FILE_NAME)->None:
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    self.dataset_parameters = json.load(file)
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")

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
        # print(self.conversational_data)

        # for category, template_question in self.question_templates.items():
        #     for courses_data in self.dataset_parameters:
        #         response = {
        #             "course_stack": None,
        #             "course_number": None,
        #             "course_name": None,
        #             "course_code": None,
        #             "faculty_name": None
        #         }
        #         response[category] = courses_data[category]
        #         for question in template_question:
        #             self.conversational_data.append({
        #                 "prompt": question.format(courses_data[category]),
        #                 "response": response
        #             })

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

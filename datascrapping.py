import json
import os
from collections import defaultdict

RAW_DATA_PATH = "raw_data/classes"
OUTPUT_DIR = "courses"

class Datascrapping:
    """
    maj list -> dump all courses -> ACC, ABC -> relevant details
    """
    def __init__(self,raw_data_path:str=RAW_DATA_PATH) -> None:
        self.major_courses_data=[]
        self.major_course_dict=defaultdict(list)
        
    def get_raw_data_from_response(self)->None:
        """
        function to pull data from response 
        and merging it into one list
        """
        folder_path = RAW_DATA_PATH
        files = os.listdir(folder_path)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.readlines()
                    class_content = json.loads(content[0]) # reading the content of the file as json object
                    self.major_courses_data.extend(class_content['classes']) # pulling classes list from the object
    
    def create_stack_course_dict(self)->None:
        """
        function to create a master dict 
        with STACK as key and COURSES as value
        """
        for classes in self.major_courses_data:
            course_stack = classes['CLAS']['SUBJECT'] # pulling course STACK from the dict
            # code to create a dict with STACK as key and list of dict as values where dict object will hold all relevant
            # data for a COURSE being offered
            self.major_course_dict[course_stack].append({
                "course_prefix": classes["SUBJECTNUMBER"], # AMT 490 - course prefix
                "course_stack": classes["CLAS"]["SUBJECT"], # AMT - course stack
                "course_stack_full_form": classes["CLAS"]["SUBJECTDESCRIPTION"], # Aeronautical Management Technology
                "course_name": classes['CLAS']['COURSETITLELONG'], # Regional Jet Operations Capstone
                "course_code": classes['CLAS']['CLASSNBR'], # 11449
                "session": classes['CLAS']['SESSIONCODE'], # A/B/C
                "term": classes['CLAS']['STRM'], # 2251 - first digit -> millenia. 2nd and 3rd digit -> last two digit of year
                                                # last digit -> semester Spring (1), Summer (4), Fall (7)
                "faculty": classes['CLAS']['INSTRUCTORSLIST'], # List of all the faculties -> ["Anthony Wende"]
                "college": classes['OFFEREDBY']['INFO']['DESCRFORMAL'], # Ira A. Fulton Schools of Engineering
                "department": classes['OFFEREDBY']['DEPARTMENT'], # Aviation Programs
                "seat_info": classes['seatInfo'], # this is a dictionary with ENRL_CAP and ENRL_TOT -> "seatInfo": { "ENRL_CAP": 28, "ENRL_TOT": 0 }
                "location": {"address": classes['LOCATIONBUILDING'][0]["ADDRESS"], "map_url": classes['LOCATIONBUILDING'][0]["URL"]},
                # {"address" : "Simulator Building 157 (Poly)", "map_url" : "http://www.asu.edu/map/interactive/?psCode=SIM"}
                # "location_descr": classes['CLAS']['DESCR'], # ASU at Polytechnic
                "campus": classes['CLAS']['CAMPUS'], # POLY
                "campus_descr": classes['CLAS']['DESCR'], # ASU at Polytechnic
                "acad_career": classes['CLAS']['ACADCAREER'], # UGRD
                "hours": classes['HOURS'], # 3
                "start_date": classes['CLAS']['STARTDATE'], # 2025-01-13 00:00:00.0
                "start_time": classes['CLAS']['STARTTIME'], # 10:30 AM
                "end_date": classes['CLAS']['ENDDATE'], # 2025-05-02 00:00:00.0
                "end_time": classes['CLAS']['ENDTIME'], # 11:45 AM
                "day_list": classes['DAYLIST'] # ["T Th"]
            })


    def export_course_list(self,output_dir:str=OUTPUT_DIR)->None:
        """
        function to export STACK file
        and store all courses offered under that STACK
        """
        folder_path = output_dir
    
        # creating folder if not exist
        os.makedirs(folder_path, exist_ok=True)
    
        # iterating over dict to create files as per STACK and COURSES under those STACK
        for stack, stack_courses in self.major_course_dict.items():
            file_name = f"{stack}.json"
            file_path = os.path.join(folder_path, file_name)
    
            # writing dict object to a json file
            with open(file_path, "w") as json_file:
                json.dump(stack_courses, json_file, indent=2)
        print(f"All course class exported sucessfully")

if __name__ == "__main__":
    ds = Datascrapping()
    ds.get_raw_data_from_response();
    ds.create_stack_course_dict();
    ds.export_course_list();

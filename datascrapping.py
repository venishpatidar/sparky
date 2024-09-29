import json
import os
# maj list -> dump all courses -> ACC, ABC -> relevant details

major_courses_data = [] # major_courses_data list of all courses raw data
major_course_dict = {} # this dict have STACK and all the relevant COURSES in that STACK


# function to pull data from response and merging it into one list
def get_raw_data_from_response():
    folder_path = "raw_data/classes"
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.readlines()
                class_content = json.loads(content[0]) # reading the content of the file as json object
                major_courses_data.extend(class_content['classes']) # pulling classes dict from the object

get_raw_data_from_response()

# function to create a master dict with STACK as key and COURSES as value
def create_stack_course_dict(major_courses_data):
    for classes in major_courses_data:
        try:
            course_stack = classes['CLAS']['SUBJECT'] # pulling course STACK from the dict
            # code to create a dict with STACK as key and list of dict as values where dict object will hold all relevant
            # data for a COURSE being offered
            if course_stack in major_course_dict.keys():
                # extend the list with the relevant data from dict
                major_course_dict[course_stack].append({
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
            else:
                # create the key and add value
                major_course_dict[course_stack] = [{
                    "course_prefix": classes["SUBJECTNUMBER"],
                    "course_stack": classes["CLAS"]["SUBJECT"],
                    "course_stack_full_form": classes["CLAS"]["SUBJECTDESCRIPTION"],
                    "course_name": classes['CLAS']['COURSETITLELONG'],
                    "course_code": classes['CLAS']['CLASSNBR'],
                    "session": classes['CLAS']['SESSIONCODE'],
                    "term": classes['CLAS']['STRM'],
                    "faculty": classes['CLAS']['INSTRUCTORSLIST'], # this is a list
                    "college": classes['OFFEREDBY']['INFO']['DESCRFORMAL'],
                    "department": classes['OFFEREDBY']['DEPARTMENT'],
                    "seat_info": classes['seatInfo'], # this is a dictionary with ENRL_CAP and ENRL_TOT
                    "location": {"address": classes['LOCATIONBUILDING'][0]["ADDRESS"], "map_url": classes['LOCATIONBUILDING'][0]["URL"]},
                    "location_descr": classes['CLAS']['DESCR'],
                    "campus": classes['CLAS']['CAMPUS'],
                    "campus_descr": classes['CLAS']['DESCR'],
                    "acad_career": classes['CLAS']['ACADCAREER'],
                    "hours": classes['HOURS'],
                    "start_date": classes['CLAS']['STARTDATE'],
                    "start_time": classes['CLAS']['STARTTIME'],
                    "end_date": classes['CLAS']['ENDDATE'],
                    "end_time": classes['CLAS']['ENDTIME'],
                    "day_list": classes['DAYLIST']
                }]
        except Exception as e:
            print(f"Error occured at fetching data from major_course_list, {e}")

create_stack_course_dict(major_courses_data=major_courses_data)
# print(len(major_course_dict))

# with open('course_dict.json', 'w') as f:
#     f.write(json.dumps(major_course_dict))


# function to create STACK file and store all courses offered under that STACK
def create_stack_files_with_courses(stack_dict):
    folder_path = "stack_and_courses/"

    # creating folder if not exist
    os.makedirs(folder_path, exist_ok=True)

    # iterating over dict to create files as per STACK and COURSES under those STACK
    for stack, stack_courses in stack_dict.items():
        file_name = f"{stack}.json"
        file_path = os.path.join(folder_path, file_name)

        # writing dict object to a json file
        with open(file_path, "w") as json_file:
            json.dump(stack_courses, json_file, indent=2)

create_stack_files_with_courses(major_course_dict)

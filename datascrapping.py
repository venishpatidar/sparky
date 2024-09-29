import json
import os
# maj list -> dump all courses -> ACC, ABC -> relevant details

# major_courses_data list of all courses raw data
major_courses_data = []

folder_path = "raw_data/classes"
files = os.listdir(folder_path)
for file_name in files:
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()
            class_content = json.loads(content[0])
            major_courses_data.extend(class_content['classes'])


major_course_dict = {}
for classes in major_courses_data:
    try:
        course_stack = classes['CLAS']['SUBJECT'] # pulling course subject from the dict
        # create dict of sub with list as values ABC : [{}, {}, {}]
        if course_stack in major_course_dict.keys():
            # extend the list with the relevant data from dict
            major_course_dict[course_stack].append({
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

print(len(major_course_dict))
with open('course_dict.json', 'w') as f:
    f.write(json.dumps(major_course_dict))
# print("major courses data", major_course_dict)

import pandas as pd
import os
import json
# set file locations
excel_location = os.path.join('Mentoring.xlsx')
args_location = os.path.join('job_args.json')
output_location = os.path.join('job.json')
# Read excel file
students = pd.read_excel(excel_location, sheet_name="Mentors").to_dict(orient='records')  # nopep8
modules = pd.read_excel(excel_location, sheet_name="Modules").to_dict(orient='records')  # nopep8
workshops = pd.read_excel(excel_location, sheet_name="Workshops").to_dict(orient='records')  # nopep8


# generate timeslot name array
timeslots = []
days = ['M', 'T', 'W', 'X', 'F']
times = ['09', '10', '11', '12', '13', '14', '15', '16', '17']
for day in days:
    for time in times:
        timeslots.append(day+time)


def cleanModuleData(modules):
    for module in modules:
        # reformat courses string to array of strings
        coursesStr = module['Course IDs']
        del module['Course IDs']
        courses = coursesStr.split(', ')
        module['Course IDs'] = courses
    return modules


def convertTimeslotsToArr(obj):
    times = []
    for timeslot in timeslots:
        times.append(obj[timeslot])
        del obj[timeslot]
    return times


def deNormalizeWSdata(workshops, modules):
    for workshop in workshops:
        module = None
        # find workshop module
        for tmp in modules:
            if tmp['Module ID'] == workshop['Module ID']:
                module = tmp

        if module:
            # handle adding module data to ws
            workshop['Module Name'] = module['Module']
            workshop['Module Level'] = module['Level']
            workshop['Course IDs'] = module['Course IDs']
    return workshops


modules = cleanModuleData(modules)

workshops = deNormalizeWSdata(workshops, modules)

# print(students[0])
print(workshops[0])

# add ids to workshops and students to be used in job file
for i in range(0, len(workshops)):
    workshops[i]["id"] = i
    # clean workshop infor
    del workshops[i]['Comment']
    workshops[i]["Timeslots"] = convertTimeslotsToArr(workshops[i])


for i in range(0, len(students)):
    students[i]["id"] = i
    students[i]["Timeslots"] = convertTimeslotsToArr(students[i])


# delete job file and generate new one
with open(output_location, 'w') as f:
    job = {
        "nodes": students,
        "groups": workshops
    }

    with open(args_location) as args_file:
        job_args = json.load(args_file)

    job['alg_params'] = job_args['alg_params']
    job['costing_params'] = job_args['costing_params']

    json.dump(job, f)

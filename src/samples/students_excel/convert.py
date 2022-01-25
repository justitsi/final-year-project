from numpy import append
import pandas as pd
import os
import json

# define Workshop names and target size in order to generate label data dynamically
workshops = ['A', 'B', 'C']
WS_GROUP_SIZE = 5
WS_MIN_SIZE = 3
# define how many proposals are included in each student row
NODE_NUM_PROPOSALS = WS_GROUP_SIZE - 1


# set file locations
excel_location = os.path.join('Groups.xlsx')
args_location = os.path.join('job_args.json')
output_location = os.path.join('job.json')
# Read excel file
students = pd.read_excel(excel_location, sheet_name="Requests").to_dict(orient='records')  # nopep8


def cleanStudentData(student, numOfProposals):
    # convert student proposals to arrayof values
    proposals = []
    for i in range(1, numOfProposals+1):
        if (student[f'Proposal {i}']):
            if not (pd.isna(student[f'Proposal {i}'])):
                proposals.append(int(student[f'Proposal {i}']))
        del student[f'Proposal {i}']

    student['Proposals'] = proposals

    # clear non-secuential student ids
    student['GID'] = student['ID']
    del student['ID']

    # convert NaN 'Response's to None
    if pd.isna(student['Response']):
        student['Response'] = None

    return student


def generateJobLabels(WSNames, WSCounts, tSize, minSize):
    job_labels = []
    cnt = 0
    # generate group names based on workshop name, size and target group size
    for i in range(0, len(WSNames)):
        count = WSCounts[i]
        for k in range(0, int(count/tSize)):
            job_labels.append({
                'id': cnt,
                'Workshop': WSNames[i],
                'GroupNum': k,
                'NameFull': f'{WSNames[i]}{k}',
                'MinSize': minSize
            })
            cnt += 1
    return job_labels


# generate job
job_nodes = []

workshopCnt = [0, 0, 0]

for i in range(0, len(students)):
    student = cleanStudentData(students[i], NODE_NUM_PROPOSALS)
    student['id'] = i

    job_nodes.append(student)
    workshopCnt[workshops.index(student['Workshop'])] += 1


job_groups = generateJobLabels(workshops, workshopCnt, WS_GROUP_SIZE, WS_MIN_SIZE)  # nopep8

# delete job file and generate new one
with open(output_location, 'w') as f:
    job = {
        "nodes": job_nodes,
        "groups": job_groups
    }

    with open(args_location) as args_file:
        job_args = json.load(args_file)

    job['alg_params'] = job_args['alg_params']
    job['costing_params'] = job_args['costing_params']

    json.dump(job, f)

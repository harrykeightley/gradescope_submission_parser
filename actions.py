import os
from pprint import pprint
from typing import Dict
from pathlib import Path

def print_submission_info(submission_info):
    pprint(submission_info)

def rename_by_student_number(submission_info, input_folder, output_folder):
    student_number = submission_info.get(':sid', submission_info.get(':name'))
    student_folder = os.path.join(output_folder, student_number)
    Path(student_folder).mkdir(parents=True, exist_ok=True)

    a2 = os.path.join(input_folder, submission_info["submission"], "a2.py")
    os.system(f'cp {a2} {student_folder}')

    _store_submission_info_file(submission_info, student_folder)

def group_by_section(submission_info, input_folder, output_folder):
    section = submission_info.get('Section', 'no_section').replace(' ', '_').lower()
    section_folder = os.path.join(output_folder, section)
    Path(section_folder).mkdir(parents=True, exist_ok=True)

    a2 = os.path.join(input_folder, submission_info["submission"], "a2.py")
    name = submission_info.get(":name").replace(' ', '_').lower()
    os.system(f'cp {a2} {os.path.join(section_folder, name)}.py')

def _store_submission_info_file(submission_info, folder):
    with open(os.path.join(folder, 'info'), 'w') as file:
        file.writelines(str(x) for x in submission_info.items())
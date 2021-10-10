import argparse
import os
import sys
import yaml
from manifest_parser import *
from actions import *
from tqdm import tqdm

MANIFEST = 'submission_metadata.yml'
DEFAULT_OUTPUT_FOLDER = os.getcwd() 

# Actions
ZIP = "zip-by-section"
RENAME = "rename"
GROUP = "group"
PRINT = "print"
ACTIONS = [RENAME, GROUP, PRINT]

def main():
    # Commandline arguments
    parser = argparse.ArgumentParser(description="Perform actions on exported gradescope submissions")
    parser.add_argument("submissions", 
            help="The folder to generate zipped submissions from")
    parser.add_argument("actions", choices=ACTIONS)
    parser.add_argument("-o", "--output-folder", dest="output_folder", default=DEFAULT_OUTPUT_FOLDER,
            help="Zipped submissions output folder")

    args = parser.parse_args()
    
    input_folder = args.submissions
    output_folder = args.output_folder
    action = args.actions

    # Argument error handling
    if not os.path.isdir(input_folder):
        print("Not a valid input folder", file=sys.stderr)
        parser.print_usage()
        return

    if not os.path.isdir(input_folder):
        print("Not a valid output folder", file=sys.stderr)
        parser.print_usage()
        return
    
    if not os.path.isfile(os.path.join(input_folder, MANIFEST)):
        print(f'{MANIFEST} not found within {input_folder}', file=sys.stderr)
        parser.print_usage()
        return

    # Parse manifest and perform actions
    if action == PRINT:
        parse(input_folder, print_submission_info)
    if action == RENAME:
        parse(input_folder, lambda x: rename_by_student_number(x, input_folder, output_folder))
    if action == GROUP:
        parse(input_folder, lambda x: group_by_section(x, input_folder, output_folder))


def parse(input_folder: str, handler): 
    manifest = os.path.join(input_folder, MANIFEST)
    total_submissions = len(os.listdir(input_folder)) - 1

    raw = None

    with tqdm(total=total_submissions) as pbar: # progress bar
        with open(manifest) as wrapper:
            for event in yaml.parse(wrapper):
                if raw is None:
                    if isinstance(event, yaml.ScalarEvent):
                        raw = RawSubmission(event)
                    continue
            
                raw.add_event(event)
                if raw.is_complete():
                    tree = generate_tree(raw.get_events())
                    info = clean(tree, raw.get_submission_number())
                    handler(info)
                    raw = None
                    pbar.update(1)


if __name__ == "__main__":
    main()
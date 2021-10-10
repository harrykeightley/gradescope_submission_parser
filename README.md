# gradescope_submission_parser
A program for performing actions on bundled gradescope submissions.

## Why is this important?
Gradescope seems to bundle all metadata for student submissions into a single (illegible) file.
When student enrollments are in the hundreds, this can result in a single file which is 6GB+.
This small program defines a way of parsing the `submissions_metadata.yaml` file and performing actions based on the
representation our parser creates.

## Installation
1. Requires `pipenv` for dependency management.
2. Clone the directory
3. `cd` within it
4. `pipenv install && pipenv shell`

## Usage
There are only a few predefined actions on the submissions right now:
1. `print`: Prints the 'cleaned' submission data to `stdout`
2. `rename`: Reorganises students into folders based on their student id.
3. `group`: Groups student submissions into folders based on their section and name.

Use `python3 main.py -h` (or `py main.py -h` on windows) to see usage options.

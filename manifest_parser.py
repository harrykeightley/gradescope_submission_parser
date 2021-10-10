from typing import Dict, List
import yaml
import sys

START_EVENTS = yaml.MappingStartEvent, yaml.SequenceStartEvent
END_EVENTS = yaml.MappingEndEvent, yaml.SequenceEndEvent

class RawSubmission:

    def __init__(self, start_event: yaml.ScalarEvent) -> None:
        self._counter = -1 
        self._start = start_event.value
        self._events = []

    def has_started(self):
        return self._counter >= 0

    def is_complete(self):
        return self._counter == 0

    def add_event(self, event):
        if not self.has_started():
            self._counter = 0

        self._events.append(event)
        if isinstance(event, yaml.MappingStartEvent):
            self._counter += 1
        if isinstance(event, yaml.MappingEndEvent):
            self._counter -= 1
    
    def get_submission_number(self):
        return self._start

    def get_events(self):
        return self._events
        

def generate_tree(events: List[yaml.NodeEvent]) -> Dict:
    """ Turns a sequence of yaml events into python data types. """
    stack = []
    data = {}

    for i, event in enumerate(events):
        if any([isinstance(event, x) for x in START_EVENTS]):
            stack.append(event)
            data[event] = []

        if isinstance(event, yaml.ScalarEvent):
            data[stack[-1]].append(event.value)

        if any([isinstance(event, x) for x in END_EVENTS]):
            start = stack.pop()
            next_data = _collate_data(event, data[start])

            if len(stack) == 0:
                return next_data
            data[stack[-1]].append(next_data)

def _collate_data(event, data):
    if isinstance(event, yaml.MappingEndEvent):
        result = {}
        for i in range(len(data) // 2):
            result[data[2 * i]] = data[2 * i + 1]
        return result

    # Otherwise it must have been a sequence expression    
    return data
   
def clean(submission_data: Dict, submission_number: str):
    # submission_data.pop(':history') # clean 
    # if 'tests' in submission_data[':results']:
    #     submission_data[':results'].pop('tests')
    if len(submission_data[':submitters']) > 1:
        print(f'Multiple submitters for submission: {submission_number}', sys.stderr)
    result = {k: v for (k, v) in submission_data[':submitters'][-1].items()}
    result['submission'] = submission_number
    return result

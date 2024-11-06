
import json
from typing import List

import config
from model import Issue

# Store issues as singleton to avoid reloads
_ISSUES:List[Issue] = None

class DataLoader:
    """
    Loads the issue data into a runtime object.
    """
    
    def __init__(self):
        """
        Constructor
        """
        self.data_path:str = config.get_parameter('ENPM611_PROJECT_DATA_PATH')
        
    def get_issues(self):
        """
        This should be invoked by other parts of the application to get access
        to the issues in the data file.
        """
        global _ISSUES # to access it within the function
        if _ISSUES is None:
            _ISSUES = self._load()
            print(f'Loaded {len(_ISSUES)} issues from {self.data_path}.')
        self._clean_issues()
        return _ISSUES
    
    def _clean_issues(self):
        """
        Removes problematic data from issues
        """
        # Remove null events
        global _ISSUES
        for issue in _ISSUES:
            # 2 issues have null text
            if issue.text is None:
                issue.text = ""
            
            # 188 issues have null authors and event_date
            for event in list(issue.events):
                if event.author is None or event.event_date is None:
                    issue.events.remove(event)
        
        

    def _load(self):
        """
        Loads the issues into memory.
        """
        with open(self.data_path,'r') as fin:
            return [Issue(i) for i in json.load(fin)]
    

if __name__ == '__main__':
    # Run the loader for testing
    DataLoader().get_issues()
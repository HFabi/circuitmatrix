class StatusMessage:
    """This class implements a mycroft status message"""

    def __init__(self, status):
        self.status = status
    
    def __str__(self):
        return self.status

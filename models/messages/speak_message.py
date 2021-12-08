class SpeakMessage:
    """This class implements a viseme message"""

    def __init__(self, text, mood, startTime, visemes):
        self.text = text
        self.mood = mood
        self.startTime = startTime
        self.visemes = visemes
        
    def __str__(self):
        return self.text + " " + self.mood + " at startTime:" + self.startTime + " with "+ self.visemes
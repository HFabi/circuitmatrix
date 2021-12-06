class SpeakMessage:
    """This class implements a viseme message"""

    def __init__(self, text, mood, startTime, visemes):
        self.text = text
        self.mood = mood
        self.startTime = startTime
        self.visemes = visemes

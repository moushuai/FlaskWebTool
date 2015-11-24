
class VideoResult:
    def __init__(self):
        self.ground_truth_label = ''
        self.name = ''
        self.path = ''
        self.pre_label = ''
        self.score = ''
        self.time = ''


class ImageResult:
    def __init__(self):
        self.name = ''
        self.path = ''
        self.pre_label = ''
        self.score = ''


class Distribution:
    def __init__(self):
        self.filed = []
        self.ratio = {}


class Record:
    def __init__(self):
        self.name = ''
        self.time = ''


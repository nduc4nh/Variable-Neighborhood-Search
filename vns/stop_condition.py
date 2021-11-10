class NonImprovemnt:
    def __init__(self, stop):
        self.count = 0
        self.stop = stop

    def start_over(self):
        self.count = 0

    def is_met(self):
        return self.count == self.stop
    
    def update(self):
        self.count += 1

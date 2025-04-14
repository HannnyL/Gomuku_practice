class pointscounter:
    def __init__(self):
        self.spoints = 0
        self.cpoints = 0
    def increse_point(self,flag):
        if flag == 's':
            self.spoints += 1
        elif flag == 'c':
            self.cpoints += 1

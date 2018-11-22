import time

class TimeTracker:
    def __init__(self, print_process=True):
        self.print_process = print_process
        self.start_time = time.time()
        self.end_time = time.time()

    def tic(self):
        self.start_time = time.time()

    def toc(self):
        self.toc('')

    def toc(self, process, tic=True):
        self.end_time = time.time()
        if self.print_process:
            print('--- %s: %0.3f sec' % (process, self.end_time - self.start_time))
        if tic:
            self.tic()

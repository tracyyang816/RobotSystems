from readerwriterlock import rwlock

class Bus:
    def __init__(self, msg = ""):
        self.msg = msg
        self.lock = rwlock.RWLockWriteD()

    
    def read(self):
        with self.lock.gen_wlock():
            msg = self.msg
            return msg

    
    def write(self, new_msg):
        with self.lock.gen_wlock():
            self.msg = new_msg
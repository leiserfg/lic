class boomer(object):

    def __init__(self, fn):
        self.fn = fn

    def __format__(self, *args, **kargs):
        if not hasattr(self, 'val'):
            self.val = self.fn()
        return self.val.__format__(*args, **kargs)

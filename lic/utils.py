

class boomer(object):

    def __new__(cls, source):
        for method in ['str', 'format', 'repr']:
            method = '__%s__' % method

            def m(obj, *args, **kargs):
                try:
                    return obj._intern
                except:
                    obj._intern = source()
                    return obj._intern

            setattr(cls, method, m)

        return object.__new__(cls)

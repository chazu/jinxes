def listify(gen):
    "Convert a generator into a function which returns a list"
    def patched(*args, **kwargs):
        return list(gen(*args, **kwargs))
    return patched

@listify
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def multiIndex(the_object, index_array):
    """
    TODO Write this docstring
    """
    return reduce(lambda obj, key: obj[key], index_array, the_object)

def multiIndexAssign(the_object, index_array, value):
    """
    Assign to a multi-indexed hash key
    """
    if type(index_array) == str:
        index_array = list(index_array)

    last = index_array.pop()
    if len(index_array) == 0:
        the_object[last] = value
    else:
        target = multiIndex(the_object, index_array)
        target[last] = value

def isDict(thing):
    return type(thing) == dict

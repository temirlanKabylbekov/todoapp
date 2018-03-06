from functools import wraps


def autosave(fn):
    """
    Automatically run save() after the decorated method
    """
    @wraps(fn)
    def decorated(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        self.save()
        return result

    return decorated

from pydoc import classname


def restrict_access(class_name: str):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            if str(self.__class__.__name__) != class_name:
                raise PermissionError(f"{method.__name__} can only be accessed by {class_name}.")
            return method(self, *args, **kwargs)
        return wrapper
    return decorator

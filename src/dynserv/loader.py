from importlib import import_module

def import_from_path(class_path: str):
    """
    Imports a class or function from a given module path.

    Args:
        class_path (str): The path to the class or function in the format 'module.sub:ClassName'.

    Returns:
        Any: The imported class or function object.

    Raises:
        ValueError: If the class_path does not contain a ':' separator.
        ImportError: If the specified object is not found in the module.

    Example:
        >>> MyClass = import_from_path('my_package.my_module:MyClass')
    """
    if ":" not in class_path:
        raise ValueError(f"Invalid class_path '{class_path}'. Expected 'module.sub:ClassName'")
    module_path, obj_name = class_path.split(":", 1)
    module = import_module(module_path)
    try:
        return getattr(module, obj_name)
    except AttributeError as e:
        raise ImportError(f"Object '{obj_name}' not found in module '{module_path}'") from e

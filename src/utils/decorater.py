from functools import wraps
import os
from pathlib import Path

from src.utils.logger import get_logger

# def chdir_to_project_root(project_root='mlops_sp'):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             p = Path('.').resolve()

#             while p != p.parent: 
#                 print(p.name)
#                 if p.name == project_root:
#                     os.chdir(p)
#                     break
#                 p = p.parent
#             else:
#                 raise FileNotFoundError(f"Directory '{project_root}' not found.")

#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

def use_log(func):
    @wraps(func)
    def wrapped_logger(*args, **kwargs):
        logger = get_logger()
        try:
            result = func(logger, *args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error occurred in function '{func.__name__}': {str(e)}")
            raise
    return wrapped_logger

if __name__ == "__main__": 
    @chdir_to_project_root('mlops_sp')
    def my_function():
        print(f"Running in directory: {os.getcwd()}")
    my_function()
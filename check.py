from flask import redrect, session
from functools import wraps

def login_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' in session:
             return func(*args, **kwargs)
        else:
            return redirect('/')
    return wrapper

def normal_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' not in session:
             return func(*args, **kwargs)
        else:
            return redirect('/login/')
    return wrapper


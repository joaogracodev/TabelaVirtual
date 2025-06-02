from flask import session, redirect

from functools import wraps

def check_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'turma' in session:
            return func(*args, **kwargs)
        return redirect('/login')
    return wrapper

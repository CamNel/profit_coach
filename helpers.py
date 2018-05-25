# Profit Coach

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///profitcoach.db")


def login_required(f):
    # Requires user is logged in to access
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Code source from a repsonse to a stack overflow question
def formatter(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

# Check none function
def checkNone(value):
    # If the value passed in is not an int then return it as an int being 0
    if (type(value) is not int):
        x = 0
    else:
        x = int(round(value))

    return x
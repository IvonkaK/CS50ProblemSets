import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

import re


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

# check username for illegal chars
def isUsernameValid(username):

    # use regex for username check
    char_reg = re.compile(r'(\w{4,})') # check if username has at least 4 characters
    char_reg_value = char_reg.findall(username)

    if char_reg_value == [] or username.isalnum() == False:
        return False
    return True

# check password strength
def isPasswordStrong(password):

    # use regex for password strength check
    char_reg = re.compile(r'(\w{6,})') # check if password has at least 6 characters
    lower_reg = re.compile(r'[a-z]+') # check if at least one lowercase letter
    upper_reg = re.compile(r'[A-Z]+') # check if atleast one upper case letter
    digit_reg = re.compile(r'[0-9]+') # check if at least one digit.
    space_reg = re.compile(r'[\s]') # check for white spaces

    char_reg_value = char_reg.findall(password)
    lower_reg_value = lower_reg.findall(password)
    upper_reg_value = upper_reg.findall(password)
    digit_reg_value = digit_reg.findall(password)
    space_reg_value = space_reg.findall(password)

    if char_reg_value == [] or lower_reg_value == [] or upper_reg_value == [] or digit_reg_value == [] or space_reg_value != []:
        return False
    return True

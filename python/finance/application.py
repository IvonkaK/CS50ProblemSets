import os
import json
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, isUsernameValid, isPasswordStrong

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # get current logged-in user id
    user_id = session["user_id"]

    # get all user's stocks from buys table and cash total from users table
    result_buys = db.execute("SELECT symbol, name, price, shares FROM buys WHERE user_id= :user_id", user_id=user_id)

    total = []
    # get current price of each stock user owns
    for item in result_buys:
        data = lookup(item['symbol'])
        item['price'] = data['price']

        # add total value per each bought stock
        item['total'] = data['price'] * item['shares']

        # total spent per stock
        total.append(item['total'])


    # user's cash balance
    cash = db.execute("SELECT cash FROM users WHERE id= :user_id", user_id=user_id)
    cash_balance = round(cash[0]["cash"], 2)

    # user's grand total (i.e., stocks’ total value plus cash)
    grand_total = sum(total) + cash_balance

    for element in result_buys:
        element['price'] = usd(element['price'])
        element['total'] = usd(element['total'])

    return render_template("index.html", result=result_buys, cash=usd(cash_balance), total=usd(grand_total))


# buy a share
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # get current logged in user id
    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get data from api based on a symbol
        data = request.form.get("symbol")
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        # look up api data
        quote = lookup(data)
        if not quote:
            return apology("symbol does not exist, provide existing symbol", 403)

        # get quantity of shares user wants to buy
        quantity = request.form.get("shares")
        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares", 403)

        total_price = quote['price'] * float(quantity)

        # check in db if user has enough money
        total_cash = db.execute("SELECT cash FROM users WHERE id= :user_id", user_id=user_id)
        total_cash_value = total_cash[0]["cash"]

        if total_cash_value < total_price:
            return apology("you don't have enough money to buy this number of stock", 403)
        else:

            # check if user already bought that company shares, if yes update shares and time
            has_user_shares = db.execute("SELECT * FROM buys WHERE user_id= :user_id AND symbol = :symbol", user_id=user_id, symbol=data.capitalize())

            if not has_user_shares:
                # get current datetime to save the timestamp of the transaction
                transacted = datetime.datetime.now()

                # buy the stock result save in db table 'buys'
                result_insert = db.execute("INSERT INTO buys (user_id, symbol, name, shares, price, transacted) VALUES ( :user_id, :symbol, :name, :shares, :price, :transacted)",
                user_id=user_id, symbol=quote['symbol'], name=quote['name'], shares=quantity, price=quote['price'], transacted=transacted)
                if result_insert is None:
                    return apology("could not insert stock data into buys", 403)

                # reduce users total cash of the stock price they bought
                user_cash_updated = total_cash_value - total_price

                result_update = db.execute("UPDATE users SET cash = :value WHERE id= :user_id", value=user_cash_updated, user_id=user_id)
                if result_update is None:
                    return apology("could not update user's cash", 403)

                # add record to history table
                result_add = db.execute("INSERT INTO history (user_id, symbol, shares, price, transacted, action) VALUES ( :user_id, :symbol,:shares, :price, :transacted, :action)",
                user_id=user_id, symbol=quote['symbol'], shares=quantity, price=quote['price'], transacted=transacted, action='B')

                if result_add is None:
                    return apology("could not insert values into history", 403)

                # Redirect user to home page
                return redirect("/")

            # if user has already shares, update the number of shares and timestamp of the transaction
            else:
                shares_number = has_user_shares[0]['shares']
                new_number_of_shares = shares_number + int(quantity)

                transacted = datetime.datetime.now()
                result_update = db.execute("UPDATE buys SET shares= :shares, transacted= :transacted WHERE user_id= :user_id AND symbol= :symbol", shares=new_number_of_shares, transacted=transacted, user_id=user_id, symbol=data.capitalize())

                if result_update is None:
                    return apology("could not update stock data", 403)

                # reduce user's total cash of the stock price they bought
                user_cash_updated = total_cash_value - total_price

                cash_update = db.execute("UPDATE users SET cash = :value WHERE id= :user_id", value=user_cash_updated, user_id=user_id)
                if cash_update is None:
                    return apology("could not update user's cash", 403)

                # add buy record to history table
                add_history = db.execute("INSERT INTO history (user_id, symbol, shares, price, transacted, action) VALUES ( :user_id, :symbol,:shares, :price, :transacted, :action)",
                user_id=user_id, symbol=quote['symbol'], shares=quantity, price=quote['price'], transacted=transacted, action='B')

                if add_history is None:
                    return apology("could not insert values into history", 403)

                # Redirect user to home page
                return redirect("/")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # get current logged-in user id
    user_id = session["user_id"]

    # get user history data
    history_data = db.execute("SELECT symbol, shares, price, transacted, action FROM history WHERE user_id= :user_id", user_id=user_id)

    for item in history_data:
        item['price'] = usd(item['price'])
        if item['action'] == 'B':
            item['action'] = 'Bought'
        else:
            item['action'] = 'Sold'
            item['shares'] = "-" + str(item['shares'])

    return render_template("history.html", history_data=history_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# get a quote from api
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get data from api based on a symbol
        data = request.form.get("symbol")

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        quote = lookup(data)
        if not quote:
            return apology("symbol does not exist, provide existing symbol", 403)


        # extract name, price and symbl of the quoted stock
        name = quote['name']
        price = usd(quote['price'])
        symbol = quote['symbol']

        # Redirect user to quoted page with values
        return render_template("quoted.html", name=name, price=price, symbol=symbol)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


# register new user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        username = request.form.get("username")

        # check for uniquenes of username
        username_unique = db.execute("SELECT username FROM users WHERE username= :username", username=username)
        if username_unique:
            return apology("username must be unique", 403)

        if isUsernameValid(username) == False:
            return apology("username can only contain letters and numbers with no space, must also contain at least 4 characters", 403)


        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        password =  request.form.get("password")

        # check for strong password
        if isPasswordStrong(password) == False:
            return apology("password must include: at least 6 characters, one lowercase letter, one uppercase letters, one digit, no spaces", 403)

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        confirmation = request.form.get("confirmation")

        if not password == confirmation:
            return apology("pasword and confirmation must be the same", 403)

        # hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)


        # Create new user record in DB
        rows = db.execute("INSERT INTO users (username, hash, cash) VALUES ( :username, :hashed_password, '10000.00')",
        username=request.form.get("username"), hashed_password=hashed_password)

        if rows is None:
            return apology("could not create new user", 403)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # get current logged-in user id
    user_id = session["user_id"]

    # get all symbols of stocks own by user
    data = db.execute("SELECT symbol FROM buys WHERE user_id= :user_id", user_id=user_id)
    symbols = []
    for symbol in data:
        symbols.append(symbol['symbol'])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get symbol and share number user wants to sell
        symbol = request.form.get("symbol")
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        shares_number = request.form.get("shares")
        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares", 403)

        # get current datetime to save the timestamp of the transaction
        transacted = datetime.datetime.now()

        # get data from api based on a symbol
        data = request.form.get("symbol")
        quote = lookup(data)
        latest_price = round(quote['price'])

        # get total money user will get when sellling
        total_earned = latest_price * int(shares_number)

        # select and update user's shares in buys table based on user id and symbol
        current_shares = db.execute("SELECT shares FROM buys WHERE user_id= :user_id AND symbol= :symbol", user_id=user_id, symbol=symbol)

        # check if user has number of shares they want to sell
        if current_shares[0]['shares'] < int(shares_number):
            return apology("You don't have that many shares to sell. Your current number of shares is: %d" %current_shares[0]['shares'], 403)

        updated_shares = current_shares[0]['shares'] - int(shares_number)
        result_update_shares = db.execute("UPDATE buys SET shares= :shares WHERE user_id= :user_id AND symbol= :symbol", shares=updated_shares, user_id=user_id, symbol=symbol)

        if result_update_shares is None:
            return apology("could not update user's shares", 403)

        # get cash balance from user
        cash_balance = db.execute("SELECT cash FROM users WHERE id= :user_id", user_id=user_id)

        updated_cash_balance = cash_balance[0]['cash'] + int(total_earned)

        # update cash balance with new value
        result_update_cash = db.execute("UPDATE users SET cash= :cash WHERE id= :user_id", cash=updated_cash_balance, user_id=user_id)

        if result_update_cash is None:
            return apology("could not update user's cash", 403)

        # save sold data to table sell
        result_insert_sells = db.execute("INSERT INTO sells (user_id, symbol, name, shares_sold, price, transacted) VALUES ( :user_id, :symbol, :name, :shares_sold, :price, :transacted)",
                user_id=user_id, symbol=quote['symbol'], name=quote['name'], shares_sold=shares_number, price=quote['price'], transacted=transacted)

        if result_insert_sells is None:
            return apology("could not insert user's sells", 403)

        # add sell record to history table
        result_insert_history = db.execute("INSERT INTO history (user_id, symbol, shares, price, transacted, action) VALUES ( :user_id, :symbol,:shares, :price, :transacted, :action)",
        user_id=user_id, symbol=quote['symbol'], shares=shares_number, price=quote['price'], transacted=transacted, action='S')

        if result_insert_history is None:
            return apology("could not insert user's history", 403)

        #if user's shares number is 0 remove the record from buys completely
        total_shares = db.execute("SELECT shares FROM buys WHERE user_id= :user_id AND symbol= :symbol", user_id=user_id, symbol=symbol)
        if total_shares[0]['shares'] == 0:
            result_delete = db.execute("DELETE FROM buys WHERE user_id= :user_id AND symbol= :symbol", user_id=user_id, symbol=symbol)

            if result_delete != 1:
                return apology("could not remove the record", 403)

        # redirect to homepage where the updated data appears
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", symbols=symbols)


# change password
@app.route("/password-change", methods=["GET", "POST"])
def passwordChage():
    """Change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure current password was submitted
        elif not request.form.get("current-password"):
            return apology("must provide current password", 403)

        # Ensure new password was submitted
        elif not request.form.get("new-password"):
            return apology("must provide new password", 403)

        username = request.form.get("username")
        current_password = request.form.get("current-password")
        new_password = request.form.get("new-password")


        # find user based on username and current password provided
        result = db.execute("SELECT * FROM users WHERE username= :username", username=username)
        if len(result) != 1:
            return apology("invalid username", 403)

        elif not check_password_hash(result[0]["hash"], current_password):
            return apology("current password is incorrect", 403)

        # check for strong password
        if isPasswordStrong(new_password) == False:
            return apology("Password must include: at least 6 characters, one lowercase letter, one uppercase letters, one digit, no space", 403)

        # update user's password
        user_id = result[0]['id']
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        result = db.execute("UPDATE users SET hash= :hashed_password WHERE id= :user_id", hashed_password=hashed_password, user_id=user_id)
        if result is None:
            return apology("password was not updated", 403)

        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password-change.html")


# add money to an account
@app.route("/add-money", methods=["GET", "POST"])
@login_required
def addMoney():

    # get current logged-in user id
    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("amount"):
            return apology("must specify amount to be added", 403)

        amount = request.form.get("amount")

         # get cash balance from user
        cash_balance = db.execute("SELECT cash FROM users WHERE id= :user_id", user_id=user_id)

        updated_cash_balance = cash_balance[0]['cash'] + int(amount)

        # update cash balance with new value
        result_update_cash = db.execute("UPDATE users SET cash= :cash WHERE id= :user_id", cash=updated_cash_balance, user_id=user_id)

        if result_update_cash is None:
            return apology("could not update user's cash", 403)

        # redirect to homepage where the updated data appears
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add-money.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


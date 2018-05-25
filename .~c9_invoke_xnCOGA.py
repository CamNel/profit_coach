#ProfitCoach

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///profitcoach.db")


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("index.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("index.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("index.html")\

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return render_template("index.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        # Clears any lingering sessions
        session.clear()

        # Hash's the user's inputted password for protection
        hash = generate_password_hash(request.form.get("password"))

        # Inserts the register information into the user table
        result = db.execute("INSERT INTO users (username, hash, email, phone) VALUES(:username, :hash, :email, :phone)",
                            username=request.form.get("username"), hash=hash, email=request.form.get("email"), phone=request.form.get("phone"))

        db.execute("INSERT INTO profile (id) VALUES (:id)", id=result["id"])
        db.execute("INSERT INTO rmp (id) VALUES (:id)", id=result["id"])
        db.execute("INSERT INTO mga (id) VALUES (:id)", id=result["id"])
        db.execute("INSERT INTO el (id) VALUES (:id)", id=result["id"])

        Session["username"] = username=request.form.get("username")

        # Sets the user's session_id
        session["user_id"] = result["id"]
        return redirect("/profile")

    else:
        return render_template("index.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":

        db.execute("UPDATE profile SET companyname = :companyname, streetaddress = :streetaddress, city = :city, state = :state, zipcode = :zipcode, contactname = :contactname, title = :title, industry = :industry, businessstruct = :businessstruct, yearsinbusiness = :yearsinbusiness WHERE id = :user_id",
                    user_id=session["user_id"], companyname=request.form.get("companyname"), streetaddress=request.form.get("streetaddress"), city=request.form.get("city"), state=request.form.get("state"), zip=request.form.get("zip"), contactname=request.form.get("contactname"), title=request.form.get("title"), industry=request.form.get("industry"), businessstruct=request.form.get("businessstruct"), yearsinbusiness=request.form.get("yearsinbusiness"), productdescription=request.form.get("productdescription"))

        db.execute("UPDATE rmp SET 17revenue = :17revenue, 16revenue = :16revenue, 15revenue = :15revenue, grossmargin = :grossmargin, product1title = :product1title, product2title = :product2title, product3title = :product3title, product4title = :product4title, product5title = :product5title, product1ppu = :product1ppu, product2ppu = :product2ppu, product3ppu = :product3ppu, product4ppu = :product4ppu, product5ppu = :product5ppu, product1units = :product1units, product2units = :product2units, product3units = :product3units, product4units = :product4units, product5units = :product5units, product1gm = :product1gm, product2gm = :product2gm, product3gm = :product3gm, product4gm = :product4gm, product5gm = :product5gm, productdescription = :productdescription WHERE id = user_id",
                   user_id=session["user-id"], 17revenue=request.form.get("17revenue"), 16revenue=request.form.get("16revenue"), 15revenue=-request.form.get("15revenue"), grossmargin = request.form.get("averagemargin"), product1title = request.form.get("product1"), product2title = request.form.get("product2"), product3title = request.form.get("product3"), product4title = request.form.get("product4"), product5title = request.form.get("product5"), product1ppu = request.form.get("product1ppu"), product2ppu = request.form.get("product2ppu"), product3ppu = request.form.get("product3ppu"), product4ppu = request.form.get("product4ppu"), product5ppu = request.form.get("product5ppu"), product1units = request.form.get("product1units"), product2units = request.form.get("product2units"), product3units = request.form.get("product3units"), product4units = request.form.get("product4units"), product5units = request.form.get("product5units"), product1gm = request.form.get("product1gm"), product2gm = request.form.get("product2gm"), product3gm = request.form.get("product3gm"), product4gm = request.form.get("product4gm"), product5gm = request.form.get("product5gm"), productdescription = request.form.get("productdescription"))

        db.execute("UP")
    else:
        return render_template("profile.html")



# Route to perform query on if username is already in database
@app.route("/username", methods=["POST"])
def username():
    taken = False
    user = request.args.get('username')
    # retrieves the username of currently registering user
    count = db.execute("SELECT COUNT(username) FROM users WHERE username = :username", username=user)
    if (count[0]["COUNT(username)"]):
        taken = True
        return jsonify(taken)
    return jsonify(taken)


# Route to perform query on if username is already in database
@app.route("/email", methods=["POST"])
def email():
    taken = False
    email = request.args.get('email')
    # retrieves the username of currently registering user
    count = db.execute("SELECT COUNT(email) FROM users WHERE email = :email", email=email)
    if (count[0]["COUNT(email)"]):
        taken = True
        return jsonify(taken)
    return jsonify(taken)

# Validates user login information
@app.route("/loginCheck", methods=["POST"])
def loginCheck():
    userNotValid = False
    # Collects the username on the pass from javascript
    username = request.args.get('username')
    # Collects the password from javascript
    pasword = request.args.get('password')

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = :username",
                      username=request.form.get("username"))

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        userNotValid = True

    return jsonify(userValid)





















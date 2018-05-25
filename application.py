#ProfitCoach

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, abort
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, checkNone, formatter

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
    # Renders the home page template
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs the user in"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("index.html", error=true, message="Must enter username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("index.html", error=true, message="Must Enter passsword")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("index.html", error=True, message="Username or Password Incorrect")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Once logged in the user will be fed into the analysis page to pick up where left off
        return redirect("/analysis")
    # If the user goes via get then they are redirected home
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    """Registers the user"""

    if request.method == "POST":
        # Clears any lingering sessions
        session.clear()

        """Error checking on server if javascript fails"""
        # Checks if user submitted username
        if not request.form.get("username"):
            return render_template("index.html", error=True, message="Must submit username")
        # Checks to ensure user input a password
        if not request.form.get("password"):
            return render_template("index.html", error=True, message="Please enter password")
        # Checks to ensure user input the password confirmation
        if not request.form.get("confirmation"):
            return render_template("index.html", error=True, message="Must submit confirmation")
        # Checks to ensure the user's password and password confirmation match
        if not request.form.get("password") == request.form.get("confirmation"):
            return render_template("index.html", error=True, message="Password and confirmation must match")

        # Hash's the user's inputted password for protection
        hash = generate_password_hash(request.form.get("password"))

        # Inserts the register information into the user table
        result = db.execute("INSERT INTO users (username, hash, email, phone) VALUES(:username, :hash, :email, :phone)",
                            username=request.form.get("username"), hash=hash, email=request.form.get("email"), phone=request.form.get("phone"))
        # Insert the user_id into each of the database table to create a row for user so that they may later update values
        db.execute("INSERT INTO profile (id) VALUES (:id)", id=result)
        db.execute("INSERT INTO rmp (id) VALUES (:id)", id=result)
        db.execute("INSERT INTO mga (id) VALUES (:id)", id=result)
        db.execute("INSERT INTO el (id) VALUES (:id)", id=result)

        # Sets the user's session_id
        session["user_id"] = result
        # Redirects user to the profile input page
        return redirect("/profile")
    # If user reaches register via get they are redirected to home where they can click the register popup
    else:
        return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Updates database user tables with profile info"""
    if request.method == "POST":
        """Needs server form checking here"""

        # Updates user's rows in each of the database tables
        db.execute("UPDATE profile SET companyname = :companyname, streetaddress = :streetaddress, city = :city, state = :state, zipcode = :zipcode, contactname = :contactname, title = :title, industry = :industry, businessstruct = :businessstruct, yearsinbusiness = :yearsinbusiness, submitted = :submitted, consultation = :consultation WHERE id = :user_id",
                    user_id=session["user_id"], companyname=request.form.get("companyname"), streetaddress=request.form.get("streetaddress"), city=request.form.get("city"), state=request.form.get("state"), zipcode=request.form.get("zip"), contactname=request.form.get("contactname"), title=request.form.get("title"), industry=request.form.get("industry"), businessstruct=request.form.get("businessstruct"), yearsinbusiness=request.form.get("yearsinbusiness"), submitted = "true", consultation = request.form.get("consultation"))

        db.execute("UPDATE mga SET meals = :meals, webmarketing = :web, marketingcost = :marketingcost, emailmarketing = :emailmarketing, socialmediamarketing = :socialmediamarketing, wordofmouth = :wordofmouth, othermarketing = :othermarketing, generalcost = :generalcost, insurancecost = :insurancecost, desiredprofit = :desiredprofit WHERE id = :user_id",
                    user_id=session["user_id"], meals=request.form.get("mealsentertainment"), marketingcost=request.form.get("marketingcost"), emailmarketing=request.form.get("emailpercentage"), web=request.form.get("webpercentage"), socialmediamarketing=request.form.get("socialpercentage"), wordofmouth=request.form.get("wompercentage"), othermarketing=request.form.get("otherpercentage"), generalcost=request.form.get("generalcost"), insurancecost=request.form.get("insurance"), desiredprofit = request.form.get("desiredprofit"))

        db.execute("UPDATE el SET executiveee = :executiveee, executivecomp = :executivecomp, manageree = :manageree, managercomp = :managercomp, salesee = :salesee, salescomp = :salescomp, serviceee = :serviceee, servicecomp = :servicecomp, adminee = :adminee, admincomp = :admincomp, payroll = :payroll, ownrent = :ownrent, sqfootage = :sqfootage, rent = :rent, camcharges = :camcharges, utilitycost = :utilitycost, benefits = :benefits WHERE id = :user_id",
                    user_id=session["user_id"], executiveee=request.form.get("owneree"), executivecomp=request.form.get("ownercomp"), managercomp=request.form.get("managercomp"), manageree=request.form.get("manageree"), salesee=request.form.get("salesee"), salescomp=request.form.get("salescomp"), serviceee=request.form.get("servicee"), rent=request.form.get("monthly"), servicecomp=request.form.get("servicecomp"), adminee=request.form.get("adminee"), admincomp=request.form.get("admincomp"), payroll=request.form.get("payroll"), benefits=request.form.get("benefits"), ownrent=request.form.get("ownrent"), sqfootage=request.form.get("sqfootage"), camcharges=request.form.get("camcharges"), utilitycost=request.form.get("utilitycost"))

        db.execute("UPDATE rmp SET productdescription = :productdescription, sevenrevenue = :sevenrevenue, sixrevenue = :sixrevenue, fiverevenue = :fiverevenue, grossmargin = :grossmargin, product1title = :product1title, product2title = :product2title, product3title = :product3title, product4title = :product4title, product5title = :product5title, product1ppu = :product1ppu, product2ppu = :product2ppu, product3ppu = :product3ppu, product4ppu = :product4ppu, product5ppu = :product5ppu, product1units = :product1units, product2units = :product2units, product3units = :product3units, product4units = :product4units, product5units = :product5units, product1gm = :product1gm, product2gm = :product2gm, product3gm = :product3gm, product4gm = :product4gm, product5gm = :product5gm WHERE id = :user_id",
                    user_id=session["user_id"], productdescription=request.form.get("productdescription"), sevenrevenue=request.form.get("sevenrevenue"), sixrevenue=request.form.get("sixrevenue"), fiverevenue=request.form.get("fiverevenue"), grossmargin=request.form.get("averagemargin"), product1title=request.form.get("product1"), product2title=request.form.get("product2"), product3title=request.form.get("product3"), product4title=request.form.get("product4"), product5title=request.form.get("product5"), product1ppu=request.form.get("product1ppu"), product2ppu=request.form.get("product2ppu"), product3ppu=request.form.get("product3ppu"), product4ppu=request.form.get("product4ppu"), product5ppu=request.form.get("product5ppu"), product1units=request.form.get("product1units"), product2units=request.form.get("product2units"), product3units=request.form.get("product3units"), product4units=request.form.get("product4units"), product5units=request.form.get("product5units"), product1gm=request.form.get("product1gm"), product2gm=request.form.get("product2gm"), product3gm=request.form.get("product3gm"), product4gm=request.form.get("product4gm"), product5gm=request.form.get("product5gm"))

        # User now now completed the profile and are ready to move on to analysis information page
        return redirect("/analysisinfo")

    # If reaches profile via get this will render the profile template page
    else:
        return render_template("profile.html")




# Route to perform query on if username is already in database
@app.route("/username", methods=["POST"])
def username():
    # Sets initial variable of taken to false
    taken = False
    # Gets the username input value via the args through ajax request
    user = request.args.get('username')
    # retrieves the username of currently registering user
    count = db.execute("SELECT COUNT(username) FROM users WHERE username = :username", username=user)
    # If there is a user with this username then switch taken to be true and return the jsonify of taken
    if (count[0]["COUNT(username)"]):
        taken = True
        return jsonify(taken)
    # Returns the jsonify of taken at this point with taken still false. Meaning no username with that value exists
    return jsonify(taken)


# Route to perform query on if username is already in database
@app.route("/email", methods=["POST"])
def email():
    # Similar to username establishes taken variable
    taken = False
    # Retrieves the input email via args
    email = request.args.get('email')
    # retrieves the email of currently registering user
    count = db.execute("SELECT COUNT(email) FROM users WHERE email = :email", email=email)
    # If someone is already registered with this email then return taken true
    if (count[0]["COUNT(email)"]):
        taken = True
        return jsonify(taken)
    # Email is not taken
    return jsonify(taken)

# Validates user login information
@app.route("/logincheck", methods=["POST"])
def loginCheck():
    # Variable to return to figure out if user is in database with that password
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
    # Returns the variable to figure out whether the user is valid or not
    return jsonify(userValid)

# An error handler to disallow user to reach analysis page if form is not filled out first
@app.errorhandler(428)
def form_not_filled(error):
    # Sets the notsubmitted variable to true triggering a popup in html
    return render_template("profile.html", notsubmitted = True)


# Route for the analysis page
@app.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    # Collects the user_id into a variable to use
    user_id = session["user_id"]
    # Query the profile data base and store row as variable profile
    profile = db.execute("SELECT * FROM profile WHERE id = :user_id",
                user_id=user_id)
    # If the user has not submitted the profile form then aborts with a 428
    if (profile[0]["submitted"] == "false"):
        abort(428)

    # Creates analysis dictionary
    analysis = dict()
    # Sets the contact and company name key value in analysis
    analysis["contact"] = profile[0]["contactname"]
    analysis["company"] = profile[0]["companyname"]

    # Queries the other databases saving the user's unique row in each as a variable
    el = db.execute("SELECT * FROM el WHERE id = :user_id",
                     user_id=user_id)

    rmp = db.execute("SELECT * FROM rmp WHERE id = :user_id",
                      user_id=user_id)

    mga = db.execute("SELECT * FROM mga WHERE id = :user_id",
                      user_id=user_id)

    industry = db.execute("SELECT * FROM industry WHERE industry = :industry",
                           industry=profile[0]["industry"])

    # Calls a helper checkNone function that handles a variable that is not an integer and sets to zero
    camcharges = checkNone(el[0]["camcharges"])
    utilitycost = checkNone(el[0]["utilitycost"])
    insurance = checkNone(mga[0]["insurancecost"])
    rent = checkNone(el[0]["rent"])
    general_cost = checkNone(mga[0]["generalcost"])
    desired_profit = checkNone(mga[0]["desiredprofit"])
    executiveee = checkNone(el[0]["executiveee"])
    executivecomp = checkNone(el[0]["executivecomp"])
    manageree = checkNone(el[0]["manageree"])
    managercomp = checkNone(el[0]["managercomp"])
    salesee = checkNone(el[0]["salesee"])
    salescomp = checkNone(el[0]["salescomp"])
    serviceee = checkNone(el[0]["serviceee"])
    servicecomp = checkNone(el[0]["servicecomp"])
    adminee = checkNone(el[0]["adminee"])
    admincomp = checkNone(el[0]["admincomp"])

    # Adds desired profit to the analysis dict
    analysis["desiredprofit"] = desired_profit

    # Gets the gm target ppercentage from the industry table. This value is based on what the industry ideal percentage is
    gm_target_percentage = round(industry[0]["gm"])
    # Adds to the analysis dict
    analysis["gmpercentagetarget"] = gm_target_percentage

    # Total general admin costs for year. General costs plus supplies
    actual_general_admin = round((general_cost * 12) + (insurance))
    # Adds to the analysis dict
    analysis["GAC"] = actual_general_admin

    # Totals of all the occupancy costs
    occupancy = round((camcharges * 12) + (utilitycost * 12) + (rent * 12))
    # Adds to the analysis dict
    analysis["occupancy"] = occupancy

    # Calculates the target for gross margin in dollars. based on the user's goal profit and fixed cost and take in the industry ideals for compensation and marketing
    gm_target = round((actual_general_admin + desired_profit + occupancy) / (1 - ((industry[0]["compensation"] / 100) + (industry[0]["marketing"] / 100))))
    # Adds to the analysis dict
    analysis["target_gmdollars"] = gm_target
    #Sets the analysis target revenue using the gross margin dollars and gross margin percentage
    analysis["target_revenue"] = round(gm_target / (gm_target_percentage / 100))

    # Calculate the target amount of compensation spending
    compensation_target = round(gm_target * (industry[0]["compensation"] / 100))
    analysis["target_comp"] = compensation_target

    # Calculates the target amount of marketing spending based on approximate industry averages
    marketing_target = gm_target * (industry[0]["marketing"] / 100)
    analysis["target_marketing"] = (marketing_target)
    # Sets the target cost of sales  equal to target revenue minus target gross margin dollars
    analysis["target_cost_sales"] = round(analysis["target_revenue"] - analysis["target_gmdollars"])
    # Sets the target total expenses equal to the totals of fixed costs and variable costs
    analysis["target_total_expenses"] = round(analysis["GAC"] + analysis["occupancy"] + analysis["target_marketing"] + analysis["target_comp"])
    # All of the equatations for the percentages. With cost of sales and gross margin being based on revenue and the others based on gross margin dollars
    analysis["target_cost_salespercentage"] = round(analysis["target_cost_sales"] / analysis["target_revenue"] * 100)
    analysis["target_gmpercentage"] = round(analysis["target_gmdollars"] / analysis["target_revenue"] * 100)
    analysis["target_comppercentage"] = industry[0]["compensation"]
    analysis["target_occupancypercentage"] = round(analysis["occupancy"] / analysis["target_gmdollars"] * 100)
    analysis["target_marketingpercentage"] = industry[0]["marketing"]
    analysis["targetGAC_percentage"] = round(analysis["GAC"] / analysis["target_gmdollars"] * 100)
    analysis["target_expensepercentage"] = round(analysis["target_total_expenses"] / analysis["target_gmdollars"] * 100)
    analysis["target_profitpercentage"] = round(analysis["desiredprofit"] / analysis["target_gmdollars"] * 100)


    # Sets the current revenue takes into account the years in business. Knowing that the user is required to put in different inputs depending on how long they have been in business
    if (profile[0]["yearsinbusiness"] == 0):
        current_revenue = 0
    elif (profile[0]["yearsinbusiness"] == 1):
        current_revenue = rmp[0]["sevenrevenue"]
    elif (profile[0]["yearsinbusiness"] == 2):
        current_revenue = (rmp[0]["sevenrevenue"] + rmp[0]["sixrevenue"]) / 2
    else:
        current_revenue = ((rmp[0]["sevenrevenue"] + rmp[0]["sixrevenue"] + rmp[0]["fiverevenue"]) / 3)

    # If the company has never been in business it sets the appropriate values equal to N/A knowing that the user won't have filled them out
    if (profile[0]["yearsinbusiness"] == 0):
        analysis["current_revenue"] = "N/A"
        analysis["current_cost_sales"] = "N/A"
        analysis["current_gmdollars"] = "N/A"
        analysis["current_marketing"] = "N/A"
        analysis["current_comp"] = "N/A"
        analysis["total_expenses"] = "N/A"
        analysis["current_profit"] = "N/A"
        analysis["current_revenuepercentage"] = "N/A"
        analysis["current_cost_salespercentage"] = "N/A"
        analysis["current_gmpercentage"] = "N/A"
        analysis["current_comppercentage"] = "N/A"
        analysis["occupancypercentage"] = "N/A"
        analysis["current_marketingpercentage"] = "N/A"
        analysis["currentGAC_percentage"] = "N/A"
        analysis["current_expensepercentage"] = "N/A"
        analysis["current_profitpercentage"] = "N/A"
        analysis["revenue_difference"] = "N/A"
        analysis["cost_of_sales_difference"] = "N/A"
        analysis["gross_margin_difference"] = "N/A"
        analysis["occupancy_difference"] = 0
        analysis["marketing_difference"] = "N/A"
        analysis["compensation_difference"] = "N/A"
        analysis["gacdifference"] = 0
        analysis["totalexpensedifference"] = "N/A"
        analysis["profitdifference"] = "N/A"

    # With the user having been in business they will have had to submit more values and we will calculate the actual amounts
    else:
        # Adds current revenue to the dict
        analysis["current_revenue"] = (current_revenue)
        # The current gross margin dollar amount is based on current revenue and the percentage gr margin amount that the user gave
        analysis["current_gmdollars"] = current_revenue * (rmp[0]["grossmargin"] / 100)
        # Sets cost of sales and current marketing values based on their formulas
        analysis["current_cost_sales"] = (analysis["current_revenue"] - analysis["current_gmdollars"])
        analysis["current_marketing"] = (mga[0]["meals"] * 12) + mga[0]["marketingcost"]

        # Totals up all the possible employee types to get total compensation
        employee_comp = (executiveee * executivecomp) + (manageree * managercomp) + (salesee * salescomp) + (serviceee * servicecomp) + (adminee * admincomp)

        # Sets benefits with the checknone function to ensure all math operators function in future
        benefits = checkNone(el[0]["benefits"])
        # If the for some reason the javascript assigning of payroll did not work out this makes sure it is defaulted to 15 percent
        if (el[0]["payroll"] == None or el[0]["payroll"] == ""):
            payroll_percentage = 15
        else:
            payroll_percentage = el[0]["payroll"]
        # Calculates the monetary amount of payroll tax burden
        payroll_burden = round(employee_comp * (payroll_percentage / 100))
        # Calculates the current compensation as the pay to employees plus the benefits the user uses and plus the payroll burden
        analysis["current_comp"] = (employee_comp + benefits + payroll_burden)
        # Sets total expenses as a sum of all the variable and fixed expenses
        analysis["total_expenses"] = analysis["current_comp"] + analysis["current_marketing"] + analysis["occupancy"] + analysis["GAC"]
        # Profit equal to the gm dollars which already takes into account cost of sales and then subtracts total expenses
        analysis["current_profit"] = analysis["current_gmdollars"] - analysis["total_expenses"]

        # Sets the current user's percentage values
        analysis["current_revenuepercentage"] = 100
        analysis["current_cost_salespercentage"] = round(analysis["current_cost_sales"] / analysis["current_revenue"] * 100)
        analysis["current_gmpercentage"] = round(analysis["current_gmdollars"] / analysis["current_revenue"] * 100)
        analysis["current_comppercentage"] = round(analysis["current_comp"] / analysis["current_gmdollars"] * 100)
        analysis["occupancypercentage"] = round(analysis["occupancy"] / analysis["current_gmdollars"] * 100)
        analysis["current_marketingpercentage"] = round(analysis["current_marketing"] / analysis["current_gmdollars"] * 100)
        analysis["currentGAC_percentage"] = round(analysis["GAC"] / analysis["current_gmdollars"] * 100)
        analysis["current_expensepercentage"] = round(analysis["total_expenses"] / analysis["current_gmdollars"] * 100)
        analysis["current_profitpercentage"] = round(analysis["current_profit"] / analysis["current_gmdollars"] * 100)

        # Sets the difference between the goal gameplan and the actual business values
        analysis["revenue_difference"] = round((analysis["target_revenue"] - analysis["current_revenue"]) / analysis["current_revenue"] * 100)
        analysis["cost_of_sales_difference"] = round((analysis["target_cost_sales"] - analysis["current_cost_sales"]) / analysis["current_cost_sales"] * 100)
        analysis["gross_margin_difference"] = round((analysis["target_gmdollars"] - analysis["current_gmdollars"]) / analysis["current_gmdollars"] * 100)
        analysis["occupancy_difference"] = 0
        analysis["gacdifference"] = 0
        analysis["totalexpensedifference"] = round((analysis["target_total_expenses"] - analysis["total_expenses"]) / analysis["total_expenses"] * 100)
        analysis["profitdifference"] = round((analysis["desiredprofit"] - analysis["current_profit"]) / analysis["current_profit"] * 100)

        # If the user does not currently do marketing then just say the difference is N/A. The user is not required to enter marketing or compensation costs currently
        if (analysis["current_marketing"] == 0):
            analysis["marketing_difference"] == "N/A"
        else:
            analysis["marketing_difference"] = round((analysis["target_marketing"] - analysis["current_marketing"]) / analysis["current_marketing"] * 100)
        # Same thing as with current marketing for the compensation difference
        if (analysis["current_comp"] == 0):
            analysis["compensation_difference"] = "N/A"
        else:
            analysis["compensation_difference"] = round((analysis["target_comp"] - analysis["current_comp"]) / analysis["current_comp"] * 100)

    # If the user is not in business this makes sure that the formatter function from helpers is not formatting a N/A value
    if (profile[0]["yearsinbusiness"] != 0):
        analysis["total_expenses"] = formatter(analysis["total_expenses"])
        analysis["current_revenue"] = formatter(analysis["current_revenue"])
        analysis["current_cost_sales"] = formatter(analysis["current_cost_sales"])
        analysis["current_gmdollars"] = formatter(analysis["current_gmdollars"])
        analysis["current_comp"] = formatter(analysis["current_comp"])
        analysis["current_marketing"] = formatter(analysis["current_marketing"])
        analysis["occupancy"] = formatter(analysis["occupancy"])
        analysis["current_profit"] = formatter(analysis["current_profit"])
        # Sets the revenue percentages for user's having been in business to 100
        analysis["revenuespercentages"] = 100
    # if the user is not in business their current field will not be populated so this sets revenues percentages
    else:
        analysis["revenuespercentages"] = "N/A"

    # Runs formatter function on all of the target and required fields that no matter what will have integer values
    analysis["GAC"] = formatter(analysis["GAC"])
    analysis["desiredprofit"] = formatter(analysis["desiredprofit"])
    analysis["target_revenue"] = formatter(analysis["target_revenue"])
    analysis["target_total_expenses"] = formatter(analysis["target_total_expenses"])
    analysis["target_cost_sales"] = formatter(analysis["target_cost_sales"])
    analysis["target_gmdollars"] = formatter(analysis["target_gmdollars"])
    analysis["target_comp"] = formatter(analysis["target_comp"])
    analysis["target_marketing"] = formatter(analysis["target_marketing"])

    # Renders the analysis template passing through the analysis dict
    return render_template("analysis.html", analysis=analysis)

# Route for the analysis information path
@app.route("/analysisinfo", methods=["POST", "GET"])
@login_required
def analysisinfo():
    return render_template("analysisinfo.html")


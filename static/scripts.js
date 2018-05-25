// Error message format
function swalError(message) {
    // Calls sweet alert inside swalError function allowing user to pass messgae
    swal({
        title: `<h3>${message}</h3>`,
        type: 'error',
        timer: 1500,
        width: 400,
        padding: 100,
        showConfirmButton: false
    });
}

// Function in case user goes to analysis before having filled out profile
function submitSwal() {
    swalError("Complete Form");
}

// Function to run the employee compensation values through in registration validation
function compCheck(value, comp){
    // Sets the pay variable equal to the parameter value using number to convert type
    var pay = Number(value)
    // If the parameter is not a number or is abnormally large or small
    if (isNaN(pay) || pay > 5000000 || pay < 3500){
        // If the user left the compensation section blank set it to zero to allow math
        if (pay == "")
        {
            value = 0
        }
        // For any other reason that input is abnormal then stop form submission and show alert
        else
        {
            swalError("Abnormal Compensation Amount");
            document.profile.comp.focus();
            return false;
        }
    }
    // Sets value of the given comp in form to itself but with number function called on it and removing non digit values or decimal points
    value = Number(value.replace(/[^0-9 || /./]/g, ''));
}

// Function to update the number of employees in the profile form employee table
function updateEmployees() {
    // Calls expression and calls number function
    var owneree = Number(document.profile.owneree.value.replace(/[^0-9 || /./]/g, ''));
    var manageree = Number(document.profile.manageree.value.replace(/[^0-9 || /./]/g, ''));
    var salesee = Number(document.profile.salesee.value.replace(/[^0-9 || /./]/g, ''));
    var serviceee = Number(document.profile.serviceee.value.replace(/[^0-9 || /./]/g, ''));
    var adminee = Number(document.profile.adminee.value.replace(/[^0-9 || /./]/g, ''));
    // Adds up all the employee numbers
    var totalEmployees = owneree + manageree + salesee + serviceee + adminee;
    if (isNaN(totalEmployees))
    {
        // If the value of total employees is not a number for some reason show this statment
        totalEmployees = "Enter # of employees!";
    }
    // Display this html inside the employee table
    $("#employeesnumber").html(`<h6>${totalEmployees} Employees`);
}

// Updates the employee compensation
function updateComps() {
    // Uses the compensation for each section and the total number of employees to get the average
    var ownercomp = Number(document.profile.ownercomp.value.replace(/[^0-9 || /./]/g, ''));
    var managercomp = Number(document.profile.managercomp.value.replace(/[^0-9 || /./]/g, ''));
    var salescomp = Number(document.profile.salescomp.value.replace(/[^0-9 || /./]/g, ''));
    var servicecomp = Number(document.profile.servicecomp.value.replace(/[^0-9 || /./]/g, ''));
    var admincomp = Number(document.profile.admincomp.value.replace(/[^0-9 || /./]/g, ''));
    var owneree = Number(document.profile.owneree.value.replace(/[^0-9 || /./]/g, ''));
    var manageree = Number(document.profile.manageree.value.replace(/[^0-9 || /./]/g, ''));
    var salesee = Number(document.profile.salesee.value.replace(/[^0-9 || /./]/g, ''));
    var serviceee = Number(document.profile.serviceee.value.replace(/[^0-9 || /./]/g, ''));
    var adminee = Number(document.profile.adminee.value.replace(/[^0-9 || /./]/g, ''));

    // If the user has given an employee compensation but there are no employees in the count alter the value of number of employees
    if (ownercomp > 0 && !(owneree > 0)) {
        document.profile.owneree.value = 1;
    }
    if (managercomp > 0 && !(manageree > 0)) {
        document.profile.manageree.value = 1;
    }
    if (salescomp > 0 && !(salesee > 0)) {
        document.profile.salesee.value = 1;
    }
    if (servicecomp > 0 && !(serviceee > 0)) {
        document.profile.serviceee.value = 1;
    }
    if (admincomp > 0 && !(adminee > 0)) {
        document.profile.adminee.value = 1;
    }

    // Calculates the total average compensation across all the employee types
    var totalComp = Math.round(((ownercomp * owneree) + (managercomp * manageree) + (salescomp * salesee) + (servicecomp * serviceee) + (admincomp * adminee))/(owneree + manageree + salesee + serviceee + adminee));
    // Handles the total comp value not being a number
    if (isNaN(totalComp))
    {
        totalComp = "Enter employee compensation!";
    }
    // Sets the html in the input form
    $("#employeescomp").html(`<h6>$${totalComp}`);
}



// Function to query the sql database on the backend
function exist (type, variable) {
    var result = null;
    // ajax request with json data type using args to pass data
    $.ajax({
        type: 'POST',
        url: `/${type}?${type}=${variable}`,
        dataType: 'json',
        success: function(data) {
            result = data;
        },
        // Don't allow async
        async: false
    });
    // Return the value from the ajax request
    return result;
}

// Function to query the sql database on the backend
function existTwo (type, variable, variableTwo) {
    var result = null;
    // Ajax request with multiple parameters given
    $.ajax({
        type: 'POST',
        url: `/${type}?${variable}=${variable}&${variableTwo}=${variableTwo}`,
        dataType: 'json',
        success: function(data) {
            result = data;
        },
        async: false
    });
    return result;
}


// Check product function to handle all the different amounts of products
function checkProduct(productNum) {
    var a = `product${productNum}`;
    var b = `product${productNum}ppu`;
    var c = `product${productNum}units`;
    var d = `product${productNum}gm`;
    var productTitle = document.profile.a.value;
    var productPPU = Number(document.profile.b.value.replace(/[^0-9 || /./]/g, ''));
    var productUnits = Number(document.profile.c.value.replace(/[^0-9 || /./]/g, ''));
    var productGm = Number(document.profile.d.value.replace(/[^0-9 || /./]/g, ''));
    // Sets the title of the product to null if set blank
    if (productTitle == '') {
        document.profile.a.value = null
    }
    // Handles if the product price per unit is not a number
    if (isNaN(productPPU)) {
        if (productPPU == '' || productPPU == null) {
            document.profile.b.value = null
        }
        // If price per unit is not a number and it is not because it was left blank then require user to fix that
        else {
            swalError("Please enter Product PPU");
            document.profile.b.focus();
            return false;
        }
    }
    // Same as with price per unit
    if (isNaN(productUnits)) {
        if (productUnits == '' || productUnits == null) {
            document.profile.c.value = null;
        }
        else {
            swalError("Please enter product units");
            document.profile.c.focus();
            return false;

        }
    }
    // Same as with units and price per units but makes sure input is valid percentage amount
    if (isNaN(productGm)) {
        if (productGm == '' || productGm == null) {
            document.profile.d.value = null;
        } else if (productGm < 0 || productGm > 100) {
            swalError("Please Enter a valid gross margin value");
            document.profile.d.focus();
        } else {
            swalError("Please Enter Product Gross Margin");
            document.profile.d.focus();
            return false;
        }
    }
    // Change values to remove any non digit inputs
    document.profile.b.value = document.profile.b.value.replace(/[^0-9 || /./]/g, '');
    document.profile.c.value = document.profile.c.value.replace(/[^0-9 || /./]/g, '');
    document.profile.d.value = document.profile.d.value.replace(/[^0-9 || /./]/g, '');
}


// Function to validate login
function loginValidate() {
    var username = document.login.username.value;
    var password = document.login.password.value;
    // Calls exist function to query and check if the username and password given are for a valid user
    var userInfo = existsTwo('logincheck', username, password);

    // Checks to make sure the user gave a username input
    if (username == '')
    {
        swalError("Please enter your username");
        document.login.username.focus();
        return false;
    }

    // Checks to make sure the user entered a password
    else if (password == '')
    {
        swalError("Pleae enter your password");
        document.login.password.focus();
        return false;
    }
    // If the ajax request from the exist function returns that there is a problem with the username trying to be logged in
    else if (userInfo == true)
    {
        swalError("Username or password Incorrect");
        document.login.username.focus();
        return false;
    }
    // Allow form to go through
    else
    {
        return true;
    }
}

// Function to handle registration
function registerValidate() {
    // Changes the form values into variables
    var username = document.register.username.value;
    var password = document.register.password.value;
    var confirmation = document.register.confirmation.value;
    // Converts phone value into number handling whether or not user entered -'s or ('s
    var phone = Number(document.register.phone.value.replace(/[^0-9 || /./]/g, ''));
    var email = document.register.email.value;
    // Calls function to check if username or password are taken
    var userTaken = exist("username", username);
    var emailTaken = exist("email", email);

    // Ensures the user has entered a username
    if (username == '')
    {
        swalError("Must include username");
        document.register.username.focus();
        return false;
    }

    // Regular expression to check if user's email input is looks like it should be a valid email
    if (!/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(email))
    {
        swalError("Please provide an email address");
        document.register.email.focus();
        return false;
    }

    // Makes sure the user's input for password and confirmation match
    if (password != confirmation)
    {
        swalError("Make sure that passwords match");
        document.register.password.focus();
        return false;
    }

    // Rough check that phone number is valid
    if (phone < 10000000 || phone > 999999999999999)
    {
        swalError("Make sure you entered a valid phone number");
        document.register.phone.focus();
        return false;
    }

    // Makes sure the user entered a password at least eight characters long
    if (password.length < 8)
    {
        swalError("Password must be at least 8 characters long");
        document.register.password.focus();
        return false;
    }

    // Queries to find if the username input is already taken
    if (userTaken)
    {

        swalError("Username is taken");
        document.profile.username.focus();
        return false;
    }

    // Checks if there is already someone registered with that email
    if (emailTaken)
    {
        swalError("Already Registered with that email");
        document.register.email.focus();
        return false;
    }

    // Form submitted is valid
    else
    {
        swal({
              title: "<h3>Great</h3>",
              type: "success",
              text: "You're Registered",
              showConfirmButton: false,
              width: 400,
              padding: 100
            });
        return true;
    }
}



// Function to validate all of the profile input information
function profileValidate() {
    // Checks to ensure user entered company name
    var companyName = document.profile.companyname.value;
    if (companyName == '' || companyName == null)
    {
        swalError("Please enter a company name");
        document.profile.companyname.focus();
        return false;
    }
    // Makes sure user entered a street address
    var streetaddress = document.profile.streetaddress.value;
    if (streetaddress == '' || streetaddress == null)
    {
        swalError("Please enter a street address");
        document.profile.streetaddress.focus();
        return false;
    }
    // Ensures user entered a city
    var city = document.profile.city.value;
    if (city == '' || city == null)
    {
        swalError("Please enter a city");
        document.profile.city.focus();
        return false;
    }
    // Ensured user entered a state
    if (document.profile.state.value == '' || document.profile.state.value == null)
    {
        swalError("Please enter a state");
        document.profile.state.focus();
        return false;
    }
    // Ensure use
    var zipcode = Number(document.profile.zip.value);
    if (isNaN(zipcode) || zipcode < 10000 || zipcode > 99999)
    {
        swalError("Please enter a company name");
        document.profile.zip.focus();
        return false;
    }
    // Ensure user entered a contact name
    var contactname = document.profile.contactname.value;
    if (contactname == '' || contactname == null)
    {
        swalError("Please enter a contact name");
        document.profile.contactname.focus();
        return false;
    }
    // Make sure the user entered a title
    var title = document.profile.title.value;
    if (title == '' || title == null)
    {
        swalError("Please enter a title with company");
        document.profile.title.focus();
        return false;
    }
    // Ensures the user selected an industry
    var industry = document.profile.industry.value;
    if (industry == null || industry == '')
    {
        swalError("Please select an industry");
        document.profile.industry.focus();
        return false;
    }
    // Makes sure the user enters a business structure
    var consultation = document.profile.consultation.value;
    if (consultation == "true"){
        var businessstruct = document.profile.businessstruct.value;
        if (businessstruct == '' || businessstruct == null)
        {
            swalError("Please select a business structure");
            document.profile.businessstruct.focus();
            return false;
        }
    }

    // Checks amount of years in business to make sure it is something reasonable
    var yearsinbiz = Number(document.profile.yearsinbusiness.value);
    if (isNaN(yearsinbiz) || yearsinbiz < 0 || yearsinbiz > 200)
    {
        swalError("Please enter a valid number of years in business or 0 if none");
        document.profile.yearsinbusiness.focus();
        return false;
    }

    // Checks to make sure user has entered revenues for years they have been in business
    var sevenRevenue = Number(document.profile.sevenrevenue.value.replace(/[^0-9 || /./]/g));
    if (isNaN(sevenRevenue) || sevenRevenue == "" || sevenRevenue == null)
    {
        if (yearsinbiz > 0)
        {
            swalError("Please enter 2017 revenue");
            document.profile.sevenrevenue.focus();
            return false;
        }
    }
    var sixRevenue = Number(document.profile.sixrevenue.value.replace(/[^0-9 || /./]/g));
    if (isNaN(sixRevenue) || sixRevenue == "" || sixRevenue == null)
    {
        if (yearsinbiz > 1)
        {
            swalError("Please enter 2016 revenue");
            document.profile.sixrevenue.focus();
            return false;
        }
    }
    var fiveRevenue = Number(document.profile.fiverevenue.value.replace(/[^0-9 || /./]/g));
    if (isNaN(fiveRevenue) || fiveRevenue == "" || fiveRevenue == null)
    {
        if (yearsinbiz > 2)
        {
            swalError("Please enter 2015 revenue");
            document.profile.fiverevenue.focus();
            return false;
        }
    }

    // Makes sure the gross margin is a valid percentage number amount
    var grossMargin = Number(document.profile.averagemargin.value);
    // User must enter a valid number gross margin amount
    if (isNaN(grossMargin) || grossMargin > 99 || grossMargin < 0)
    {
            swalError("Please enter Gross Margin in digit form or leave blank");
            document.profile.averagemargin.focus();
            return false;

    }


    // Check product function on all of the possible
    checkProduct(1);
    checkProduct(2);
    checkProduct(3);
    checkProduct(4);
    checkProduct(5);
    // Calls comp check function on each of the different category of employee's compensation values
    compCheck(document.profile.ownercomp.value, ownercomp);
    compCheck(document.profile.managercomp.value, managercomp);
    compCheck(document.profile.salescomp.value, salescomp);
    compCheck(document.profile.servicecomp.value, servicecomp);
    compCheck(document.profile.admincomp.value, admincomp);

    // If the user selected that they said they did give benfits make sure they gave a valid input
    if (document.getElementById("yesbenefits").checked == true)
    {
        var benefitCost = Number(document.profile.benefitscost.value.replace(/[^0-9 || /./]/g));
        if (isNaN(benefitCost) || benefitCost == "" || benefitCost == null)
        {
            swalError("Enter Benefits Cost Amount in Numeric Form");
            document.profile.benefitscost.focus();
            return false;
        }
    }
    // Handles payroll input amount making sure entered a valid percentage number value
    var payroll = Number(document.profile.payroll.value.replace(/[^0-9 || /./]/g));
    if (isNaN(payroll) || payroll > 75 || payroll < 0){
        if (payroll == "" || payroll == null)
        {
            // If user left blank then default payroll burden to 15%
            document.profile.payroll.value = 15;
        }
        // If they entered a non Number value then require them to
        else
        {
            swalError("Enter a valid payroll percentage number or leave blank");
            document.profile.payroll.focus();
            return false;
        }
    }
    // Ensures the rent input is a valid number input
    var rent = document.profile.monthly.value
    if (isNaN(rent))
    {
        swalError("Enter a Rent. Approximate if needed.");
        document.profile.monthly.focus();
        return false;
    }
    // requires user to enter a valid occupancy value
    var occupancy = document.profile.ownrent.value;
    if (occupancy == "")
    {
        swalError("Enter a valid payroll percentage number or leave blank");
        document.profile.ownrent.focus();
        return false;
    }
    // Requires user to enter a valid sq footage and handles user entering things like commas or dollar signs
    var sqfootage = Number(document.profile.sqfootage.value.replace(/[^0-9 || /./]/g));
    if (isNaN(sqfootage))
    {
        swalError("Enter a sq footage. Approximate if needed.");
        document.profile.sqfootage.focus();
        return false;
    }
    // Ensure the user enters a valid cam charges amount. Allowing for some flexibility of user input
    var camCharges = Number(document.profile.camcharges.value.replace(/[^0-9 || /./]/g));
    if (isNaN(camCharges))
    {
        // If they left blank set equal to zero
        if (camCharges == "")
        {
            document.profile.camcharges.value = 0;
        }
        else {
            swalError("Enter CAM charges in numeric form");
        }
    }
    // Require user to enter a utlity cost amount
    var utilityCost = Number(document.profile.utilitycost.value.replace(/[^0-9 || /./]/g));
    if (isNaN(utilityCost))
    {
        swalError("Enter a number for utility cost. Approximate if needed");
        document.profile.utilitycost.focus();
        return false;
    }
    // Handle meals input and set equal to zero if they left blank
    var meals = Number(document.profile.mealsentertainment.value.replace(/[^0-9 || /./]/g));
    if (isNaN(meals))
    {
        if (meals == "")
        {
            document.profile.mealsentertainment.value = 0;
        }
        else {
            swalError("Enter a number for Meals and Entertainment or leave blank");
            document.profile.mealsentertainment.focus();
            return false;
        }
    }
    // handles marketing cost user input converting to zero if left blank
    var marketingCost = Number(document.profile.marketingcost.value.replace(/[^0-9 || /./]/g));
    if (isNaN(marketingCost))
    {
        if (marketingCost == "")
        {
            document.profile.marketingcost.value = 0;
        }
        else {
            swalError("Enter a number for Marketing Cost or leave blank");
            document.profile.marketingcost.focus();
            return false;
        }
    }
    // Requires user to enter valid general cost, allowing flexibility of user input format
    var generalCost = Number(document.profile.generalcost.value.replace(/[^0-9 || /./]/g));
    if (isNaN(generalCost))
    {
        swalError("Must enter a general cost amount. Approximate if needed");
        document.profile.generalcost.focus();
        return false;
    }
    // Handles insurance input. Setting equal to zero if left empty
    var insurance = Number(document.profile.insurance.value.replace(/[^0-9 || /./]/g));
    if (isNaN(insurance))
    {
        if (insurance == "")
        {
            document.profile.insurance.value = 0;
        }
        else {
            swalError("Enter a number for insurance Cost or leave blank");
            document.profile.insurance.focus();
            return false;
        }
    }
    // Makes sure the user entered a desired profit
    var desiredProfit = Number(document.profile.goalprofit.value.replace(/[^0-9 || /./]/g));
    if (isNaN(desiredProfit))
    {
        swalError("Must Enter a Goal Profit");
        document.profile.goalprofit.focus();
        return false;
    }
    // Sets product description equal to null if left blank
    if (document.profile.productdescription.value == "")
    {
        document.profile.productdescription.value = null;
    }

    // Converts all the user's input values into numbers (if appropriate) and removes things like commas or dollar signs
    document.profile.goalprofit.value = document.profile.goalprofit.value.replace(/[^0-9 || /./]/g);
    document.profile.insurance.value = Number(document.profile.insurance.value.replace(/[^0-9 || /./]/g));
    document.profile.monthly.value = Number(document.profile.monthyl.value.replace(/[^0-9 || /./]/g));
    document.profile.goalprofit.value = Number(document.profile.goalprofit.value.replace(/[^0-9 || /./]/g));
    document.profile.generalcost.value = Number(document.profile.generalcost.value.replace(/[^0-9 || /./]/g));
    document.profile.marketingcost.value = Number(document.profile.marketingcost.value.replace(/[^0-9 || /./]/g));
    document.profile.mealsentertainment.value = Number(document.profile.mealsentertainment.value.replace(/[^0-9 || /./]/g));
    document.profile.utilitycost.value = Number(document.profile.utilitycost.value.replace(/[^0-9 || /./]/g));
    document.profile.camcharges.value = Number(document.profile.camcharges.value.replace(/[^0-9 || /./]/g));
    document.profile.sqfootage.value = Number(document.profile.sqfootage.value.replace(/[^0-9 || /./]/g));
    document.profile.grossmargin.value = Number(document.profile.grossmargin.value);
    document.profile.zip.value = Number(document.profile.zip.value);
    document.profile.sevenrevenue.value = document.profile.sevenrevenue.value.replace(/[^0-9 || /./]/g);
    document.profile.sixrevenue.value = document.profile.sixrevenue.value.replace(/[^0-9 || /./]/g);
    document.profile.fiverevenue.value = document.profile.fiverevenue.value.replace(/[^0-9 || /./]/g);
    document.profile.averagemargin.value = document.profile.averagemargin.value.replace(/[^0-9 || /./]/g);
    document.profile.payroll.value = document.profile.payroll.value.replace(/[^0-9 || /./]/g);
    document.profile.benefitscost.value = document.profile.benefitscost.value.replace(/[^0-9 || /./]/g);
}





// Jquery code that make sure the document is ready
$(document).ready(function() {
    // Code for the login form to popup
    // Source partially from but altered https://www.adam-bray.com/2017/02/21/create-a-popup-html-login-box-with-jquery/
    $("#loginLink").click(function( event ){
        event.preventDefault();
        $("#overlayLogin").fadeToggle("fast");
      });

    // Close the login form when the login x is hit
    $(".closeLogin").click(function(){
        $("#overlayLogin").fadeToggle("fast");
    });
    // Close login form when escape key is hit
    $(document).keyup(function(e) {
        if(e.keyCode == 27 && $("#overlayLogin").css("display") != "none" ) {
            event.preventDefault();
            $("#overlayLogin").fadeToggle("fast");
        }
    });

    // Jquery code for registration form
    $("#registerLink").click(function( event ){
        event.preventDefault();
        $("#overlayRegister").fadeToggle("fast");
    });

    // Closes the register form when the close x is hit
    $(".closeRegister").click(function(){
        $("#overlayRegister").fadeToggle("fast");
    });
    // Hides the registration form overlay when escape key is hit
    $(document).keyup(function(e) {
        if(e.keyCode == 27 && $("#overlayRegister").css("display") != "none" ) {
            event.preventDefault();
            $("#overlayRegister").fadeToggle("fast");
        }
    });
    // Toggles the active class on the tabs of profile page
    $(".tabs").click(function() {
        $(".tabs").removeClass("active");
        $(this).addClass("active");
    });

    // Code for profile form tabs
    $("#tab1link").click(function() {
        $("#tab1").show();
        $("#tab2").hide();
        $("#tab3").hide();
        $("#tab4").hide();
    });

    // When second tab is clicked show that and hide the others
    $("#tab2link").click(function () {
        $("#tab2").show();
        $("#tab1").hide();
        $("#tab3").hide();
        $("#tab4").hide();
    });
    // When the third tab is selected show the third tab and hide the others
    $("#tab3link").click(function () {
        $("#tab3").show();
        $("#tab2").hide();
        $("#tab1").hide();
        $("#tab4").hide();
    });

    // When the third tab is selected show the third tab and hide the others
    $("#tab4link").click(function () {
        $("#tab4").show();
        $("#tab2").hide();
        $("#tab1").hide();
        $("#tab3").hide();
    });

    // Next button on first page clicks through to show the next tab
    $("#next1").click(function () {
        $(".tabs").removeClass("active");
        $(".tab2").addClass("active");
        $("#tab2").show();
        $('#tab1').hide();
    });

    // Next button on second page to click through to final page
    $("#next2").click(function () {
        $(".tabs").removeClass("active");
        $(".tab3").addClass("active");
        $("#tab3").show();
        $('#tab2').hide();
    });

    // When the third next button is hit then change the active tab and show the next tablink
    $("#next3").click(function () {
        $(".tabs").removeClass("active");
        $(".tab4").addClass("active");
        $("#tab4").show();
        $('#tab3').hide();
    });
    // Adds a product table row up until there are 5 possible product forms to fill out
    $("#add").click(function() {
        var rowNum = document.getElementById("producttable").rows.length;
        var newRow = document.getElementById("producttable").insertRow(-1);
        newRow.innerHTML = `<tr><td><label>${rowNum}</label></td><td><input class="form-control flat" name="product${rowNum}" placeholder="Product/Service" type="text"></td><td><input class="form-control flat" name="product${rowNum}ppu" placeholder="Price per Unit" type="text"></td><td><input class="form-control flat" name="product${rowNum}units" placeholder="# of Units" type="text"></td><td><input class="form-control flat" name="product${rowNum}gm" placeholder="Gross Margin" type="text"></td></tr>`;


    });
    // Removes the latest product column from profile product table
    $("#remove").click(function() {
        $("#producttable tbody>tr:last").remove();
    });
    // When consulation text is clicked then show the user a message and allow them to choose the yes or no option
    $(".consultation").click(function() {
        swal({
            title: "<h3>Consultation</h3>",
            type: 'question',
            text: "If you click yes, then your data will be viewed and you will recieve and even more in depth and customized gameplan",
            confirmButtonText: "I understand",
        });
        $(".consultationcheck").show();
    });

    // Whenever the benefits check class is clicked check if the radio for yes they do provide benefits is checked and if so pop up form
    $(".benefitscheck").click(function () {
        if (document.getElementById("yesbenefits").checked == true)
        {
            $("#benefitscost").show();
        }
        if (document.getElementById("nobenefits").checked == true)
        {
            $("#benefitscost").hide();
        }
    });
    // Calls the update employees and comp functions whenever the mouse moves over that table or leaves table
    $("#compensation").on('mousemove mouseout',function() {;
        updateEmployees();
        updateComps();
    });
    // Calls same functions when the tab key pressed
    $(document).keyup(function(e) {
        if(e.keyCode == 9) {
            updateEmployees();
            updateComps();
        }
    });
});



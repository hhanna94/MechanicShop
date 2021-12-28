from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.shop import Shop
from flask_app.models.employee import Employee
from flask_app.models.job import Job

# Get route to get a list of shops that will be displayed in a dropdown on the login page. This is for if the owner wants to expand and have multiple shops with different employees and customers.
@app.route('/')
def index():
    shops = Shop.get_shops()
    return render_template("index.html", shops = shops)

# Get route to display the create employee form, a list of all employes, and a list of all open jobs.
@app.route('/admin')
def admin():
    # Make sure the user is logged in, otherwise redirect them to the login page with a message that they need to log in.
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    
    # Make sure the logged in user is an admin, otherwise redirect them to the dashboard with an access denied message.
    if session["admin"] == "N":
        flash("Can only access this page as an administrator.", "admin")
        return redirect('/dashboard')
    
    data = {"shop_id": session["shop_id"]}
    employees = Employee.get_employees(data)
    jobs = Job.get_open_jobs()
    return render_template("admin.html", employees=employees, jobs=jobs)



# Post route to create a new employee. First checks to make sure that the employee passes a validation check. If it does, then the password will be hashed using BCrypt and the user will be saved to the database. The user will be redirected to the admin page.
@app.route('/create_employee', methods=["POST"])
def create_employee():
    if not Employee.validate_registration(request.form):
        return redirect('/admin')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "password": pw_hash,
        "position": request.form["position"],
        "admin": request.form["admin"]
    }
    Employee.add_employee(data)
    return redirect('/admin')

# Post route to login a user. It will first pull the data from the form, then check if the user exists in the database.  
@app.route('/login', methods=["POST"])
def login():
    data = {
        "employee_id": request.form["employee_num"],
        "shop_id": request.form["shop_num"]
    }
    employee_in_db = Employee.get_by_id(data)

    # If the user doesn't exist, then redirect to the login page with a message that it was an invalid login attempt.
    if not employee_in_db:
        flash("Invalid Employee Number, Password, or Shop", "login")
        return redirect('/')
    # If the user does exist, check if a hashed version of the password typed in matches the saved hashed password for the user. If it fails this check, redirect to the login page with a message that it was an invalid login attempt.
    if not bcrypt.check_password_hash(employee_in_db.password, request.form['password']):
        flash("Invalid Employee Number, Password, or Shop", "login")
        return redirect('/')

    # If both checks above pass, then save the employee's ID, the shop's ID, the shop's name, and whether or not the user is an Admin in session. Then redirect to the dashboard.
    session["employee_id"] = employee_in_db.id
    session["shop_id"] = employee_in_db.shop_id
    session["shop_name"] = employee_in_db.shop.name
    if employee_in_db.admin == "Y":
        session["admin"] = "Y"
    else:
        session["admin"] = "N"
    return redirect('/dashboard')

# Get route to log out a user.
@app.route('/return')
def go_back():
    session.clear()
    return redirect('/')







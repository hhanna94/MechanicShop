from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.shop import Shop
from flask_app.models.employee import Employee
from flask_app.models.job import Job

@app.route('/')
def index():
    shops = Shop.get_shops()
    return render_template("index.html", shops = shops)


@app.route('/admin')
def admin():
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    if session["admin"] == "N":
        flash("Can only access this page as an administrator.", "admin")
        return redirect('/dashboard')
    data = {"shop_id": session["shop_id"]}
    employees = Employee.get_employees(data)
    jobs = Job.get_open_jobs()
    return render_template("admin.html", employees=employees, jobs=jobs)



# Login/Registration #
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


@app.route('/login', methods=["POST"])
def login():
    data = {
        "employee_id": request.form["employee_num"],
        "shop_id": request.form["shop_num"]
    }
    employee_in_db = Employee.get_by_id(data)
    if not employee_in_db:
        flash("Invalid Employee Number, Password, or Shop", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(employee_in_db.password, request.form['password']):
        flash("Invalid Employee Number, Password, or Shop", "login")
        return redirect('/')
    session["employee_id"] = employee_in_db.id
    session["shop_id"] = employee_in_db.shop_id
    session["shop_name"] = employee_in_db.shop.name
    print(session["shop_name"])
    if employee_in_db.admin == "Y":
        session["admin"] = "Y"
    else:
        session["admin"] = "N"
    return redirect('/dashboard')

@app.route('/return')
def go_back():
    session.clear()
    return redirect('/')







from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.controllers.users import User
from flask_app.models.customer import Customer


@app.route('/customers')
def customers():
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {"shop_id": session["shop_id"]}
    customers = Customer.get_all_customers(data)
    return render_template("customers.html", customers=customers)

@app.route('/customers/<int:customer_id>')
def customer(customer_id):
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {"customer_id": customer_id}
    customer = Customer.get_customer(data)
    return render_template("customer.html", customer=customer)

@app.route('/add_customer', methods=["POST"])
def add_customer():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "birthday": request.form["birthday"],
        "shop_id": session["shop_id"]
    }
    customer_id = Customer.create_customer(data)
    return redirect(f'/customers/{customer_id}')

@app.route('/customers/<int:id>/edit', methods=["POST"])
def edit_customer(id):
    data = {
        "id": id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "birthday": request.form["birthday"],
        "phone": request.form["phone"],
        "email": request.form["email"],
    }
    Customer.edit_customer(data)
    return redirect(f'/customers/{id}')

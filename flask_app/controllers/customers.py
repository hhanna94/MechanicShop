from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.customer import Customer

# Get route to show the customers page. Renders the "customers" template.
@app.route('/customers')
def customers():
    # Make sure the user is logged in, otherwise redirect them to the login page with a message that they need to log in.
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')

    # Get a list of all customers that belong to the shop using the shop_id saved in session upon login. To be passed to the front end.
    data = {"shop_id": session["shop_id"]}
    customers = Customer.get_all_customers(data)

    return render_template("customers.html", customers=customers)


# Get route to show an individual customer. Renders the "customer" template.
@app.route('/customers/<int:customer_id>')
def customer(customer_id):
    # Make sure the user is logged in, otherwise redirect them to the login page with a message that they need to log in.
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    
    # Get the customer details using the customer_id pulled from the URL, to be passed to the front end.
    data = {"customer_id": customer_id}
    customer = Customer.get_customer(data)

    return render_template("customer.html", customer=customer)


# Post route to create a new customer, redirects to the newly created customer.
@app.route('/add_customer', methods=["POST"])
def add_customer():
    # Data pulled from the form when a user creates a customer, which is then used to create a new customer record in the database.
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "birthday": request.form["birthday"],
        "shop_id": session["shop_id"]
    }
    # When a new record is created in the database, the ID for the record is returned. We can then use this to redirect to the newly created customer.
    customer_id = Customer.create_customer(data)

    return redirect(f'/customers/{customer_id}')


#Post route to edit a customer, redirects to the edited customer page
@app.route('/customers/<int:id>/edit', methods=["POST"])
def edit_customer(id):
    # Data pulled from the form when a user creates a customer, which is then used to edit the customer record in the database.
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

from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.controllers.users import User
from flask_app.models.car import Car
from flask_app.models.employee import Employee
from flask_app.models.service import Service
from flask_app.models.job import Job
from flask_app.models.mechanic_note import Note

# Get route to display a customer's car details, renders the "car" template
@app.route('/customers/<int:customer_id>/cars/<int:car_id>')
def car(customer_id, car_id):
    # Make sure the user is logged in, otherwise redirect them to the login page with a message that they need to log in.
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    # IDs pulled from the URL and session to be used in retrieving data from the database
    data = {
        "customer_id": customer_id,
        "car_id": car_id,
        "shop_id": session["shop_id"]
    }

    # Retrieve the car information to be passed to the front end.
    car = Car.get_car(data)
    # Retrieve a list of employees to be passed to the front end, used to assign the lead mechanic for a job.
    employees = Employee.get_employees(data)
    # Retrieve a list of services that can be added to a job to be passed to the front end.
    all_services = Service.get_services()
    # Retrieve a list of all of the notes from previous jobs for the specific car to be passed to the front end.
    all_notes = Note.get_all_car_notes(data)

    return render_template("car.html", car=car, employees=employees, all_services=all_services, all_notes=all_notes)


# Post route to add a car to the database. Redirects to the car page.
@app.route('/add_car', methods=["POST"])
def add_car():
    # Data pulled from the form when a user creates a car to be used to create a new record in the database
    data = {
        "year": request.form["car-years"],
        "make": request.form["car-makes"],
        "model": request.form["car-models"],
        "trim": request.form["car-model-trims"],
        "color": request.form["color"],
        "customer_id": request.form["customer_id"],
    }
    # When a new record is created in the database, the ID for the record is returned. We can then use this to redirect to the newly created car.
    car_id = Car.create_car(data)
    return redirect(f'/customers/{data["customer_id"]}/cars/{car_id}')
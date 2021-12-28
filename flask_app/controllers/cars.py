from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.controllers.users import User
from flask_app.models.car import Car
from flask_app.models.employee import Employee
from flask_app.models.service import Service
from flask_app.models.job import Job
from flask_app.models.mechanic_note import Note

@app.route('/customers/<int:customer_id>/cars/<int:car_id>')
def car(customer_id, car_id):
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {
        "customer_id": customer_id,
        "car_id": car_id,
        "shop_id": session["shop_id"]
    }
    car = Car.get_car(data)
    employees = Employee.get_employees(data)
    all_services = Service.get_services()
    all_notes = Note.get_all_car_notes(data)
    return render_template("car.html", car=car, employees=employees, all_services=all_services, all_notes=all_notes)

@app.route('/add_car', methods=["POST"])
def add_car():
    data = {
        "year": request.form["car-years"],
        "make": request.form["car-makes"],
        "model": request.form["car-models"],
        "trim": request.form["car-model-trims"],
        "color": request.form["color"],
        "customer_id": request.form["customer_id"],
    }
    car_id = Car.create_car(data)
    return redirect(f'/customers/{data["customer_id"]}/cars/{car_id}')
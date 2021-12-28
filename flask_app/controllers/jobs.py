from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.controllers.users import User
from flask_app.models.employee import Employee
from flask_app.models.job import Job
from flask_app.models.service import Service
from flask_app.models.mechanic_note import Note
from flask_app.models.part import Part

@app.route('/dashboard')
def dashboard():
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {"employee_id": session["employee_id"], "shop_id": session["shop_id"]}
    employee = Employee.get_mechanic_open_jobs(data)
    return render_template("dashboard.html", employee=employee)

@app.route('/customers/<int:customer_id>/cars/<int:car_id>/jobs/<int:job_id>')
def job(customer_id, car_id, job_id):
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {
        "customer_id": customer_id,
        "car_id": car_id,
        "job_id": job_id
    }
    job = Job.get_job(data)
    other_services = Service.get_other_services(data)
    notes = Note.get_job_notes(data)
    job_parts = Part.get_job_parts(data)
    return render_template("job.html", job=job, other_services = other_services, notes=notes, job_parts=job_parts)

@app.route('/add_job', methods=["POST"])
def add_job():
    data = {
        "services": request.form.getlist("services"),
        "mechanic_id": request.form["employee_id"],
        "comments": request.form["comments"],
        "customer_id": request.form["customer_id"],
        "car_id": request.form["car_id"],
    }
    job_id = Job.create_job(data)
    service_data = {
        "job_id": job_id,
        "services": data["services"]
    }
    Job.add_services_to_job(service_data)
    return redirect(f'/customers/{data["customer_id"]}/cars/{data["car_id"]}')

@app.route('/customers/<int:customer_id>/cars/<int:car_id>/jobs/<int:job_id>/update_status', methods=["POST"])
def update_status(customer_id, car_id, job_id):
    data = {
        "status": request.form["status"],
        "job_id": job_id
    }
    Job.update_status(data)
    return redirect(f'/customers/{customer_id}/cars/{car_id}/jobs/{job_id}')

@app.route('/customers/<int:customer_id>/cars/<int:car_id>/jobs/<int:job_id>/add_service', methods=["POST"])
def add_service(customer_id, car_id, job_id):
    data = {
        "service_id": request.form["service"],
        "job_id": job_id
    }
    Job.add_service_to_job(data)
    return redirect(f'/customers/{customer_id}/cars/{car_id}/jobs/{job_id}')
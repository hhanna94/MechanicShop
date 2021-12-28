from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.controllers.users import User
from flask_app.models.employee import Employee
from flask_app.models.job import Job
from flask_app.models.service import Service
from flask_app.models.mechanic_note import Note
from flask_app.models.part import Part

# Get route that retrieves and displays a list of all of the logged in user's open jobs.
@app.route('/dashboard')
def dashboard():
    # Make sure the user is logged in, otherwise redirect them to the login page with a message that they need to log in.
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {"employee_id": session["employee_id"], "shop_id": session["shop_id"]}
    employee = Employee.get_mechanic_open_jobs(data)
    return render_template("dashboard.html", employee=employee)


# Get route that retrieves displays information for a specific job.
@app.route('/customers/<int:customer_id>/cars/<int:car_id>/jobs/<int:job_id>')
def job(customer_id, car_id, job_id):
    # Make sure the user is logged in, otherwise redirect them to the login page with a message that they need to log in.
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {
        "customer_id": customer_id,
        "car_id": car_id,
        "job_id": job_id
    }
    # Retrieve the job details
    job = Job.get_job(data)
    # Retrieve a list of services that have not been added to the job
    other_services = Service.get_other_services(data)
    # Retrieve all of the mechanic notes that have been added to the job
    notes = Note.get_job_notes(data)
    # Retrieve a list of parts associated with the services on a job
    job_parts = Part.get_job_parts(data)
    return render_template("job.html", job=job, other_services = other_services, notes=notes, job_parts=job_parts)


# Post route to add a job to a car, redirects back to the car page.
@app.route('/add_job', methods=["POST"])
def add_job():
    # Use the data from the form to create a job. Save the newly created job's ID.
    data = {
        "services": request.form.getlist("services"),
        "mechanic_id": request.form["employee_id"],
        "comments": request.form["comments"],
        "customer_id": request.form["customer_id"],
        "car_id": request.form["car_id"],
    }
    job_id = Job.create_job(data)

    # Using the newly created job ID, create new lines in the jobs_have_services table in the database for each service that needs to be added to the job.
    service_data = {
        "job_id": job_id,
        "services": data["services"]
    }
    Job.add_services_to_job(service_data)
    return redirect(f'/customers/{data["customer_id"]}/cars/{data["car_id"]}')


# Post route to change the status of a job. Redirects back to the job.
@app.route('/customers/<int:customer_id>/cars/<int:car_id>/jobs/<int:job_id>/update_status', methods=["POST"])
def update_status(customer_id, car_id, job_id):
    data = {
        "status": request.form["status"],
        "job_id": job_id
    }
    Job.update_status(data)
    return redirect(f'/customers/{customer_id}/cars/{car_id}/jobs/{job_id}')


# Post route to add a service to a job. Redirects back to the job.
@app.route('/customers/<int:customer_id>/cars/<int:car_id>/jobs/<int:job_id>/add_service', methods=["POST"])
def add_service(customer_id, car_id, job_id):
    data = {
        "service_id": request.form["service"],
        "job_id": job_id
    }
    Job.add_service_to_job(data)
    return redirect(f'/customers/{customer_id}/cars/{car_id}/jobs/{job_id}')
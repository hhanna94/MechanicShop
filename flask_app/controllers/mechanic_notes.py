from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.mechanic_note import Note

# Post route to add a mechanic note to a job.
@app.route('/customers/<int:customer_id>/cars/<int:car_id>/jobs/<int:job_id>/add_note', methods=["POST"])
def add_note(customer_id, car_id, job_id):
    data = {
        "car_id": car_id,
        "job_id": job_id,
        "employees_id": session["employee_id"],
        "content": request.form["note"]
    }
    Note.create_note(data)
    return redirect(f'/customers/{customer_id}/cars/{car_id}/jobs/{job_id}')

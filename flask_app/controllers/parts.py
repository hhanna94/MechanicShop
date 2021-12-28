from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.part import Part

# Get route to retrieve and display a lit of parts.
@app.route('/parts')
def parts():
    # Make sure the user is logged in, otherwise redirect them to the login page with a message that they need to log in.
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    parts = Part.get_parts()
    return render_template("parts.html", parts=parts)


# Post route to create a new part based on user entered form information.
@app.route('/add_part', methods=["POST"])
def create_part():
    data = {
        "part_name": request.form["part_name"],
        "category": request.form["category"],
        "quantity": request.form["quantity"],
        "price": request.form["price"],
    }
    Part.create_part(data)
    return redirect('/parts')


# Get route to delete a part associated with a service
@app.route('/service/<int:service_id>/part/<int:part_id>/delete')
def remove_part_from_services(service_id, part_id):
    data = {
        "service_id": service_id,
        "part_id": part_id
    }
    Part.delete_part_from_service(data)
    return redirect(f'/services/{service_id}')


# Post route to add a part to a service
@app.route('/add_part_to_service', methods=["POST"])
def add_part_to_service():
    data = {
        "part_id": request.form["part"],
        "service_id": request.form["service_id"]
    }
    Part.add_part_to_service(data)
    return redirect(f'/services/{data["service_id"]}')


# Get route to delete a part entirely
@app.route('/parts/<int:part_id>/delete')
def delete_part(part_id):
    data = {"part_id": part_id}
    Part.delete_part(data)
    return redirect('/parts')

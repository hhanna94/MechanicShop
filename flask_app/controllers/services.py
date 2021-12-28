from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.service import Service
from flask_app.models.part import Part


@app.route('/services')
def services():
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    services = Service.get_services()
    parts = Part.get_parts()
    return render_template("services.html", services=services, parts=parts)

@app.route('/create_service', methods=["POST"])
def create_service():
    data = {
        "service_name": request.form["service_name"],
        "description": request.form["description"],
        "price": request.form["price"],
        "parts": request.form.getlist("parts")
    }
    service_id = Service.create_service(data)
    part_data = {
        "service_id": service_id,
        "parts": data["parts"]
    }
    Service.add_parts_to_service(part_data)
    return redirect('/services')

@app.route('/services/<int:id>')
def service(id):
    if not "employee_id" in session:
        flash("Must be logged in to access additional pages.", "login")
        return redirect('/')
    data = {"service_id": id}
    service = Service.get_service(data)
    all_parts = Part.get_parts()
    return render_template("service.html", service=service, all_parts=all_parts)

@app.route("/edit_service/<int:id>", methods=["POST"])
def edit_service(id):
    data = {
        "service_id": id,
        "service_name": request.form["service_name"],
        "price": request.form["price"],
        "description": request.form["description"]
    }
    Service.update_service(data)
    return redirect(f"/services/{id}")

@app.route("/services/<int:service_id>/delete")
def delete_service(service_id):
    data = {"service_id": service_id}
    Service.delete_service(data)
    return redirect("/services")
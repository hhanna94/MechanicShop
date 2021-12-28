from flask_app import app
from flask_app.controllers import employees, cars, customers, jobs, services, mechanic_notes, parts


if __name__ == "__main__":
    app.run(debug=True)



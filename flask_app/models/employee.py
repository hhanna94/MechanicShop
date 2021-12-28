from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

PASSWORD_REGEX = re.compile("^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=])(?=\\S+$).{8,}$")

from flask_app.models import customer, job, employee, car, data_helper, shop

class Employee:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.position = data["position"]
        self.password = data['password']
        self.admin = data["admin"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shop_id = data['shop_id']

        self.shop = {}
        self.jobs = []
        self.mechanic_notes = []

    @classmethod
    def add_employee(cls, data):
        query = "INSERT INTO employees (first_name, last_name, position, password, admin, shop_id, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(position)s, %(password)s, %(admin)s, 1, NOW(), NOW())"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        return results
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM employees LEFT JOIN shops ON shops.id = shop_id WHERE employees.id=%(employee_id)s AND shop_id=%(shop_id)s;"
        results = connectToMySQL(cls.database_name).query_db(query,data)[0]
        employee = cls(results)
        shop_data = {
            "id": results['shops.id'],
            "name": results['name'],
            "location": results['location'],
            "created_at": results['shops.created_at'],
            "updated_at": results['shops.updated_at'],
        }
        employee.shop = shop.Shop(shop_data)
        return employee

    @classmethod
    def get_employees(cls, data):
        query = "SELECT * FROM employees WHERE shop_id=%(shop_id)s"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        employees = []
        for employee in results:
            employees.append(cls(employee))
        return employees
    
    @classmethod
    def get_mechanic_open_jobs(cls, data):
        query = '''SELECT * FROM employees
        LEFT JOIN jobs ON jobs.mechanic_id = employees.id
        LEFT JOIN cars ON jobs.car_id = cars.id
        LEFT JOIN customers ON cars.customer_id = customers.id
        WHERE employees.id = %(employee_id)s
        ORDER BY status DESC;'''
        results = connectToMySQL(cls.database_name).query_db(query, data)
        mechanic = cls(results[0])
        for row in results:
            if row['status'] == "Completed" or row['status'] == None:
                break;
            job_data = {
                "id": row["jobs.id"],
                "comments": row["comments"],
                "status": row["status"],
                "created_at": row["jobs.created_at"],
                "updated_at": row["jobs.updated_at"],
                "mechanic_id": row["mechanic_id"],
                "car_id": row["car_id"],
            }
            mechanic_job = job.Job(job_data)

            # Use a helper function to generate the car_data object that will be used to create an instance of a Car
            car_data = data_helper.Helper.car_data_builder(row)
            mechanic_job.car = car.Car(car_data)

            customer_data = {
                "id": row['customers.id'],
                "first_name": row['customers.first_name'],
                "last_name": row['customers.last_name'],
                "email": row["email"],
                "phone": row['phone'],
                "birthday": row["birthday"],
                "created_at": row['customers.created_at'],
                "updated_at": row['customers.updated_at'],
                "shop_id": row['shop_id'],
            }
            mechanic_job.car.owner = customer.Customer(customer_data)
            mechanic.jobs.append(mechanic_job)
        return mechanic

    @classmethod
    def validate_registration(cls, data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters.", "registration")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", "registration")
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("Password must be at least 8 characters, have at least one uppercase letter, one number, and one special character.", "registration")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match.", "registration")
            is_valid = False
        return is_valid

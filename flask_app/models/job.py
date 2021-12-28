from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import employee, service, customer, car, data_helper

class Job:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.comments = data["comments"]
        self.status = data["status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.mechanic_id = data["mechanic_id"]
        self.car_id = data["car_id"]

        self.services = []
        self.mechanic = {}
        self.car = {}

    # Query the database to create a job that belongs to a car and mechanic
    @classmethod
    def create_job(cls, data):
        query = "INSERT INTO jobs (comments, status, created_at, updated_at, mechanic_id, car_id) VALUES (%(comments)s, 'Not Started', NOW(), NOW(), %(mechanic_id)s, %(car_id)s)"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # Query the database to add a new line in the jobs_have_services table for every service that needs to be added to a job
    @classmethod
    def add_services_to_job(cls, data):
        for service in data["services"]:
            new_data = {
                "job_id": data["job_id"],
                "service_id": service
            }
            query = "INSERT INTO jobs_have_services (created_at, updated_at, job_id, service_id) VALUES (NOW(), NOW(), %(job_id)s, %(service_id)s);"
            results = connectToMySQL(cls.database_name).query_db(query, new_data)
        return results

    # Query the database to add a single new service for a job, to the jobs_have_services table
    @classmethod
    def add_service_to_job(cls, data):
        query = "INSERT INTO jobs_have_services (created_at, updated_at, job_id, service_id) VALUES (NOW(), NOW(), %(job_id)s, %(service_id)s);"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # Query the database to update just the status of a particular job
    @classmethod
    def update_status(cls, data):
        query = "UPDATE jobs SET status=%(status)s, updated_at=NOW() WHERE id=%(job_id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # Query the database to get all of the job information, including all of the services on the job, the parts associated with those services, the car details, the customer details, and the lead mechanic's details
    @classmethod
    def get_job(cls, data):
        query = '''SELECT * FROM jobs
        LEFT JOIN jobs_have_services ON jobs_have_services.job_id = jobs.id
        LEFT JOIN services ON jobs_have_services.service_id = services.id
        LEFT JOIN cars ON jobs.car_id = cars.id
        LEFT JOIN customers ON cars.customer_id = customers.id
        LEFT JOIN employees ON employees.id = jobs.mechanic_id
        WHERE jobs.id=%(job_id)s;'''
        results = connectToMySQL(cls.database_name).query_db(query, data)
        first_result = results[0]
        job = cls(first_result)
        for row in results:
            service_data = {
                "id": row["services.id"],
                "service_name": row["service_name"],
                "description": row["description"],
                "price": row["price"],
                "created_at": row["services.created_at"],
                "updated_at": row["services.updated_at"],
            }
            job.services.append(service.Service(service_data))
        car_data = data_helper.Helper.car_data_builder(row)
        job.car = car.Car(car_data)
        customer_data = {
            "id": first_result['customers.id'],
            "first_name": first_result['first_name'],
            "last_name": first_result['last_name'],
            "email": first_result["email"],
            "phone": first_result['phone'],
            "birthday": first_result["birthday"],
            "created_at": first_result['customers.created_at'],
            "updated_at": first_result['customers.updated_at'],
            "shop_id": first_result['shop_id'],
            "cars": ""
        }
        job.car.owner = customer.Customer(customer_data)
        mechanic_data = {
            "id": first_result['employees.id'],
            "first_name": first_result['employees.first_name'],
            "last_name": first_result['employees.last_name'],
            "position": first_result["position"],
            "password": "not available",
            "admin": first_result["admin"],
            "created_at": first_result['employees.created_at'],
            "updated_at": first_result['employees.updated_at'],
            "shop_id": first_result['shop_id'],
        }
        job.mechanic = employee.Employee(mechanic_data)
        return job


    # Query the database to get a list of all open jobs, including the car data, the owner data, and the mechanic's data
    @classmethod
    def get_open_jobs(cls):
        query = '''SELECT * FROM jobs
        LEFT JOIN cars ON jobs.car_id = cars.id
        LEFT JOIN customers ON cars.customer_id = customers.id
        LEFT JOIN employees ON employees.id = jobs.mechanic_id
        WHERE status='Not Started' OR status='In Progress'
        ORDER BY status DESC;'''
        results = connectToMySQL(cls.database_name).query_db(query)
        jobs = []
        for row in results:
            job = cls(row)
            car_data = data_helper.Helper.car_data_builder(row)
            job.car = car.Car(car_data)
            customer_data = {
                "id": row['customers.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row["email"],
                "phone": row['phone'],
                "birthday": row["birthday"],
                "created_at": row['customers.created_at'],
                "updated_at": row['customers.updated_at'],
                "shop_id": row['shop_id'],
            }
            job.car.owner = customer.Customer(customer_data)
            mechanic_data = {
                "id": row['employees.id'],
                "first_name": row['employees.first_name'],
                "last_name": row['employees.last_name'],
                "position": row["position"],
                "password": "not available",
                "admin": row["admin"],
                "created_at": row['employees.created_at'],
                "updated_at": row['employees.updated_at'],
                "shop_id": row['shop_id'],
            }
            job.mechanic = employee.Employee(mechanic_data)
            jobs.append(job)
        return jobs

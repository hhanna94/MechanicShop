from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import customer, job, employee

class Car:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data['id']
        self.year = data['year']
        self.make = data['make']
        self.model = data["model"]
        self.trim = data['trim']
        self.color = data["color"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.customer_id = data['customer_id']

        self.jobs = []
        self.mechanic_notes = []
        self.owner = {}

    @classmethod
    def create_car(cls, data):
        query = "INSERT INTO cars (year, make, model, trim, color, created_at, updated_at, customer_id) VALUES (%(year)s, %(make)s, %(model)s, %(trim)s, %(color)s, NOW(), NOW(), %(customer_id)s)"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        return results

    @classmethod
    def get_car(cls, data):
        query = '''SELECT * FROM cars 
                LEFT JOIN customers ON customers.id = cars.customer_id 
                LEFT JOIN jobs ON jobs.car_id = cars.id
                LEFT JOIN employees ON jobs.mechanic_id = employees.id
                WHERE cars.id=%(car_id)s;'''
        results = connectToMySQL(cls.database_name).query_db(query,data)
        car = cls(results[0])
        owner_data = {
            "id": results[0]['customers.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]["email"],
            "phone": results[0]['phone'],
            "birthday": results[0]["birthday"],
            "created_at": results[0]['customers.created_at'],
            "updated_at": results[0]['customers.updated_at'],
            "shop_id": results[0]['shop_id'],
        }
        for row in results:
            job_data = {
                "id": row["jobs.id"],
                "comments": row["comments"],
                "status": row["status"],
                "created_at": row["jobs.created_at"],
                "updated_at": row["jobs.updated_at"],
                "mechanic_id": row["mechanic_id"],
                "car_id": row["car_id"],
            }
            if (job_data["id"] != None):
                one_job = job.Job(job_data)
                print("job_data", one_job)
            else:
                continue
            mechanic_data = {
                "id": results[0]['employees.id'],
                "first_name": results[0]['employees.first_name'],
                "last_name": results[0]['employees.last_name'],
                "position": results[0]["position"],
                "password": "not available",
                "admin": results[0]["admin"],
                "created_at": results[0]['employees.created_at'],
                "updated_at": results[0]['employees.updated_at'],
                "shop_id": results[0]['employees.shop_id'],
            }
            one_job.mechanic = employee.Employee(mechanic_data)
            car.jobs.append(one_job)
        car.owner = customer.Customer(owner_data)
        return car
        
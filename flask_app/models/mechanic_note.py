from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import employee, service, customer, car

class Note:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.contacted_customer = data["contacted_customer"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.employees_id = data["employees_id"]
        self.job_id = data["job_id"]
        self.car_id = data["car_id"]

        self.mechanic = {}

    # Query the database to create a new note for a particular job, written by a particular employee. Belonging to a particular car.
    @classmethod
    def create_note(cls, data):
        query = "INSERT INTO mechanic_notes (content, contacted_customer, created_at, updated_at, employees_id, job_id, car_id) VALUES (%(content)s, 'N', NOW(), NOW(), %(employees_id)s, %(job_id)s, %(car_id)s);"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # Query the database to get a list of mechanic notes that belong to a certain job, including details about the mechanic who wrote the note
    @classmethod
    def get_job_notes(cls, data):
        query = "SELECT * FROM mechanic_notes LEFT JOIN employees ON employees.id = mechanic_notes.employees_id WHERE job_id=%(job_id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        notes = []
        for row in results:
            note = cls(row)
            mechanic_data = {
                "id": row['employees.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "position": row["position"],
                "password": "not available",
                "admin": row["admin"],
                "created_at": row['employees.created_at'],
                "updated_at": row['employees.updated_at'],
                "shop_id": row['shop_id'],
            }
            note.mechanic = employee.Employee(mechanic_data)
            notes.append(note)
        return notes

    # Query the database to get a list of all mechanic notes that belong to a certain car, including details about the mechanic
    @classmethod
    def get_all_car_notes(cls, data):
        query = "SELECT * FROM mechanic_notes LEFT JOIN employees ON employees.id = mechanic_notes.employees_id WHERE car_id = %(car_id)s ORDER BY mechanic_notes.created_at DESC"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        print(results)
        notes = []
        for row in results:
            note = cls(row)
            mechanic_data = {
                "id": row['employees.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "position": row["position"],
                "password": "not available",
                "admin": row["admin"],
                "created_at": row['employees.created_at'],
                "updated_at": row['employees.updated_at'],
                "shop_id": row['shop_id'],
            }
            note.mechanic = employee.Employee(mechanic_data)
            notes.append(note)
        return notes
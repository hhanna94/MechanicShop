from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import job, part

class Service:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.service_name = data["service_name"]
        self.price = data["price"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.parts = []

    # Query the database to get a list of all services
    @classmethod
    def get_services(cls):
        query = "SELECT * FROM services;"
        results = connectToMySQL(cls.database_name).query_db(query)
        services = []
        for service in results:
            services.append(cls(service))
        return services

    # Query the database to get details about a service, including all of the parts associated with that service
    @classmethod
    def get_service(cls, data):
        query = '''SELECT * FROM services
        LEFT JOIN services_have_parts ON services.id = services_have_parts.service_id
        LEFT JOIN parts ON parts.id = services_have_parts.part_id
        WHERE services.id = %(service_id)s;'''
        results = connectToMySQL(cls.database_name).query_db(query, data)
        service = cls(results[0])
        for row in results:
            part_data = {
                "id": row["parts.id"],
                "part_name": row["part_name"],
                "quantity": row["quantity"],
                "price": row["parts.price"],
                "category": row["category"],
                "created_at": row["parts.created_at"],
                "updated_at": row["parts.updated_at"],
            }
            service.parts.append(part.Part(part_data))
        return service

    # Query the database to get a list of services that have not yet been added to a particular job
    @classmethod
    def get_other_services(cls, data):
        query = '''SELECT * FROM services WHERE id NOT IN (
            SELECT services.id FROM services
            LEFT JOIN jobs_have_services ON jobs_have_services.service_id = services.id
            LEFT JOIN jobs ON jobs_have_services.job_id = jobs.id
            WHERE jobs.id = %(job_id)s);'''
        results = connectToMySQL(cls.database_name).query_db(query, data)
        services = []
        for row in results:
            services.append(cls(row))
        return services

    # Query the database to create a new service
    @classmethod
    def create_service(cls, data):
        query = "INSERT INTO services (service_name, description, price, created_at, updated_at) VALUES (%(service_name)s, %(description)s, %(price)s, NOW(), NOW())"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # Query the database to add parts to the services_have_parts table to create the association between a service and its required parts
    @classmethod
    def add_parts_to_service(cls, data):
        for part in data["parts"]:
            new_data = {
                "service_id": data["service_id"],
                "part_id": part
            }
            query = "INSERT INTO services_have_parts (created_at, updated_at, part_id, service_id) VALUES (NOW(), NOW(), %(part_id)s, %(service_id)s);"
            results = connectToMySQL(cls.database_name).query_db(query, new_data)
        return results

    # Query the database to update a service
    @classmethod
    def update_service(cls, data):
        query = "UPDATE services SET service_name=%(service_name)s, price=%(price)s, description=%(description)s, updated_at = NOW() WHERE id=%(service_id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # Query the database to delete a servicee
    @classmethod
    def delete_service(cls, data):
        query = "DELETE FROM services WHERE id=%(service_id)s"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results







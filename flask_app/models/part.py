from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import job

class Part:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.part_name = data["part_name"]
        self.quantity = data["quantity"]
        self.price = data["price"]
        self.category = data["category"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_parts(cls):
        query = "SELECT * FROM parts ORDER BY category;"
        results = connectToMySQL(cls.database_name).query_db(query)
        parts = []
        category = ""
        for row in results:
            if category != row["category"]:
                if category != "":
                    parts.append(parts_in_category)
                parts_in_category = []
                category = row["category"]
            part = cls(row)
            parts_in_category.append(part)
        parts.append(parts_in_category)
        return parts

    @classmethod
    def create_part(cls, data):
        query = "INSERT INTO parts (part_name, quantity, price, category, created_at, updated_at) VALUES (%(part_name)s, %(quantity)s, %(price)s, %(category)s, NOW(), NOW())"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def delete_part_from_service(cls, data):
        query = "DELETE FROM services_have_parts WHERE part_id = %(part_id)s AND service_id = %(service_id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def add_part_to_service(cls, data):
        query = "INSERT INTO services_have_parts (created_at, updated_at, part_id, service_id) VALUES (NOW(), NOW(), %(part_id)s, %(service_id)s);"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results
    
    @classmethod
    def delete_part(cls, data):
        query = "DELETE FROM parts WHERE id=%(part_id)s"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def get_job_parts(cls, data):
        query = '''SELECT * FROM parts
        LEFT JOIN services_have_parts ON services_have_parts.part_id = parts.id
        LEFT JOIN services ON services_have_parts.service_id = services.id
        LEFT JOIN jobs_have_services ON jobs_have_services.service_id = services.id
        WHERE jobs_have_services.job_id = %(job_id)s;'''
        results = connectToMySQL(cls.database_name).query_db(query, data)
        parts = []
        for row in results:
            parts.append(cls(row))
        return parts
        





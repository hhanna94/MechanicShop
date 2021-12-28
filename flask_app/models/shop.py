from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Shop:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.employees = []
        self.customers = []

    # Query the database to get a list of shops.
    @classmethod
    def get_shops(cls):
        query = "SELECT * FROM shops;"
        results = connectToMySQL(cls.database_name).query_db(query)
        return results
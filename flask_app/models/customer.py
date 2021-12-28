from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import car, data_helper

class Customer:
    database_name = "mechanic_shop_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data["email"]
        self.phone = data['phone']
        self.birthday = data["birthday"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shop_id = data['shop_id']

        self.cars = []

    # Method to query the database to add a customer.
    @classmethod
    def create_customer(cls, data):
        query = "INSERT INTO customers (first_name, last_name, email, phone, birthday, created_at, updated_at, shop_id) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(birthday)s, NOW(), NOW(), %(shop_id)s);"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        return results

    # Method to query the database to get a list of all customers belonging to a shop
    @classmethod
    def get_all_customers(cls, data):
        query = "SELECT * FROM customers WHERE shop_id = %(shop_id)s"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        customers = []
        for customer in results:
            customers.append(cls(customer))
        return customers

    # Method to query the database to get all details for a customer, including a list of all of their cars 
    @classmethod
    def get_customer(cls, data):
        query = "SELECT * FROM customers LEFT JOIN cars ON cars.customer_id = customers.id WHERE customers.id=%(customer_id)s;"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        customer = cls(results[0])
        for row in results:
            # Use a helper function to generate the car_data object that will be used to create an instance of a Car (if the customer has any cars)
            car_data = data_helper.Helper.car_data_builder(row)
            if (car_data["id"] != None):
                customer.cars.append(car.Car(car_data))
            else:
                break
        return customer

    # Method to query the database to update a customer
    @classmethod
    def edit_customer(cls, data):
        query = "UPDATE customers SET first_name=%(first_name)s, last_name=%(last_name)s, birthday=%(birthday)s, phone=%(phone)s, email=%(email)s, updated_at=NOW() WHERE id=%(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query,data)
        return results
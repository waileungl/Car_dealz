from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
db = "car_deal_schema"

class Cars:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.description = data['description']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.owner_id = data['owner_id']
        self.seller_name = data['first_name'] + " " + data['last_name']
        self.seller_id = data['seller_id']
        self.purchaser_id = data['purchaser_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_car(cls, data):
        query = "INSERT INTO cars(price, model, make, year, description, owner_id, seller_id, created_at, updated_at) VALUES (%(price)s, %(model)s, %(make)s, %(year)s,%(description)s, %(owner_id)s, %(seller_id)s, now(), now());"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def edit_car(cls, data):
        query = "UPDATE cars SET price = %(price)s, make = %(make)s,description = %(description)s, model = %(model)s, year = %(year)s WHERE cars.id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_info_for_dashboard(cls, data):
        #Get all cars info and their seller info from the database
        query = "SELECT * FROM cars LEFT JOIN users ON users.id = cars.seller_id;"
        cars = []
        results = connectToMySQL(db).query_db(query)
        for row in results:
            cars.append(cls(row))

        return cars

    @classmethod
    def get_car_info_pack_by_id(cls, data):
        #Get all the info of the car by car_id
        query = "SELECT cars.id AS id, price, model, make, year, description, owner_id, users.first_name as first_name, users.last_name as last_name, seller_id, purchaser_id, cars.created_at as created_at, cars.updated_at as updated_at FROM cars LEFT JOIN users ON users.id = cars.owner_id WHERE cars.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        car_info = cls(results[0])
        return car_info

    @classmethod
    def get_purchased_car_by_owner_id(cls, data):
        query = "SELECT * from cars LEFT JOIN users ON cars.purchaser_id = users.id WHERE purchaser_id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        car_info = []
        if results:
            for row in results:
                car_info.append(cls(row))
            return car_info
        return car_info

    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(car_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def purchase_car(cls, data):
        query = "UPDATE cars SET owner_id = %(user_id)s, purchaser_id = %(user_id)s WHERE id = %(car_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def validate_car(cls, data):
        is_valid = True
        if len(data["price"]) == 0:
            flash("Price must not be blank.", "add_car")
            is_valid = False
        if len(data["year"]) == 0:
            flash("Year must not be blank.", "add_car")
            is_valid = False
        if len(data["model"]) == 0:
            flash("Model must not be blank.", "add_car")
        if len(data["make"]) == 0:
            flash("Make must not be blank.", "add_car")
        if len(data["description"]) == 0:
            flash("Description must not be blank.", "add_car")
            is_valid = False
        return is_valid
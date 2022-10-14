from flask_app import app
from flask import render_template,redirect,request, session, flash
from flask_app.models.cars import Cars

@app.route('/cars/new')
def add_car():
    if 'id' not in session:
        return redirect('/')
    return render_template("add_cars.html")

@app.route('/create_car', methods = ['POST'])
def create_car():
    car_validation = Cars.validate_car(request.form)
    if not car_validation:
        return redirect('/cars/new')
    data = {
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "owner_id": session["id"],
        "purchaser_id": "null",
        "seller_id": session["id"]
    }
    Cars.create_car(data)
    return redirect("/cars")

@app.route('/cars/<int:car_id>')
def show_car(car_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        "id": car_id
    }
    return render_template("show_cars.html", car_info_pack = Cars.get_car_info_pack_by_id(data))

@app.route('/cars/edit/<int:car_id>')
def edit_car(car_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        "id": car_id
    }
    return render_template("edit_cars.html", car_info_pack = Cars.get_car_info_pack_by_id(data))

@app.route('/edit_car', methods = ['POST'])
def edit_car_submit():
    id = request.form["car_id"]
    car_validation = Cars.validate_car(request.form)
    if not car_validation:
        return redirect(f'/cars/edit/{id}')
    data = {
        "id": request.form["car_id"],
        "price": request.form["price"],
        "year": request.form["year"],
        "model": request.form["model"],
        "description": request.form["description"],
        "make": request.form["make"],
        "owner_id": session["id"]
    }
    Cars.edit_car(data)
    return redirect("/cars")

@app.route('/cars/delete/<int:car_id>')
def delete_car(car_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        "car_id": car_id,
    }
    Cars.delete_car(data)
    return redirect("/cars")

@app.route('/cars/purchase/<int:car_id>')
def purchase_car(car_id):
    if 'id' not in session:
        return redirect('/')
    data = {
        "car_id": car_id,
        "user_id": session["id"]
    }
    Cars.purchase_car(data)
    return redirect("/user/purchases")

@app.route('/user/purchases')
def show_user_purchases():
    if 'id' not in session:
        return redirect('/')
    data = {
        "id": session["id"]
    }
    return render_template("user_purchases.html", user_purchases = Cars.get_purchased_car_by_owner_id(data))
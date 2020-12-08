from flask import Flask, render_template, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#Init marshmallow
ma = Marshmallow(app)

# Produc Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True)
    stock = db.Column(db.String)
    price = db.Column(db.Integer)
    link = db.Column(db.String)
    image = db.Column(db.String)
    
    def __init__(self, name, stock, price, link, image):
        self.name = name
        self.stock = stock
        self.price = price
        self.link = link
        self.image = image

#Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'stock', 'price', 'link', 'image')
    
#Init Schema
product_schema = ProductSchema()
proudcts_schemas = ProductSchema(many=True)
    

@app.route("/", methods=["POST", "GET"])
def home(product = None):
    all_products = Product.query.all()
    result = proudcts_schemas.dump(all_products)
    
    return render_template('index.html', products=result) 

@app.route('/product', methods=["Post"])
def add_product():
    name = request.json['name']
    stock = request.json['stock']
    price = request.json['price']
    link = request.json['link']
    image = request.json['image']
    
    new_product = Product(name, stock, price, link, image)
    
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product)

#Get All Items
@app.route('/product', methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = proudcts_schemas.dump(all_products)
    
    return jsonify(result)

#Get An Items
@app.route('/product/<id>', methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route('/product/<id>', methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    
    name = request.json['name']
    stock = request.json['stock']
    price = request.json['price']
    link = request.json['link']
    image = request.json['image']
    
    product.name = name
    product.stock = stock
    product.price = price
    product.link = link
    product.image = image 
    
    db.session.commit()
    
    return product_schema.jsonify(new_item)


if __name__ == "__main__":
    app.run()
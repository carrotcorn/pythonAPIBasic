
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return 'Hello'


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {"ID": drink.id, "Name": drink.name,
                      "Description": drink.description}

        output.append(drink_data)

    return{"Drinks": output}


@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {'ID': drink.id, "Name": drink.name, "Description": drink.description}


@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'],
                  description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": f"YEETED {drink.name}"}


@app.route('/drinks/<id>', methods=['PUT'])
def edit_drink(id):
    drink = Drink.query.get(id)
    if drink is None:z
        return {"error": "not found"}

    drink.name = request.get_json().get('name')
    drink.description = request.get_json().get('description')

    db.session.commit()
    return{"message": f"Updated {drink.name}"}

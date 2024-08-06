"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Favorite
import requests
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# trae todos los people
@app.route("/people", methods=["GET"])
def get_all_people():

    people = People()
    people = people.query.all()
    people = list(map(lambda item: item.serialize(), people))

    return jsonify(people), 200


# trae el people por id
@app.route("/people/<int:people_id>", methods=["GET"])
def get_one_people(people_id):
    people = People()
    people = people.query.get(people_id)
    
    if people is None:
        raise APIException("User not found", status_code=404)
    else:
        return jsonify(people.serialize()), 200



#traer todos los usuarios
@app.route("/users", methods=["GET"])
def get_all_users():
    users = User()
    users = users.query.all()

    users = list(map(lambda item: item.serialize(), users))
    return jsonify(users), 200


# trae todos los favoritos de un usuario
@app.route("/users/favorites/<int:theid>", methods=["GET"])
def get_all_favorites_user(theid=None):
    user = User()
    user = user.query.filter_by(id=theid).first()

    return jsonify(user.serialize_fav()), 200

    # favorite = Favorite()
    # favorite = favorite.query.filter_by(user_id=theid).all()

    # print(list(map(lambda item: item.serialize(), favorite)))

    # return jsonify([]), 200



#agregamos un people a favoritos
@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_people_fav(people_id):
    user_id = 1

    fav = Favorite()
    fav.user_id = user_id
    fav.people_id = people_id
    
    db.session.add(fav)

    try:
        db.session.commit()
        return jsonify("se guardo exitosamente"), 201
    except Exception as error:
        db.session.rollback
        return jsonify("error, debes revisar"), 201




# Solo un ejemplo
@app.route("/people/population", methods=["GET"])
def get_people_population():
    #https://www.swapi.tech/api/people?page=1&limit=2
    response = requests.get("https://www.swapi.tech/api/people?page=1&limit=300")
    response = response.json()
    response = response.get("results")

    for item in response:
        result = requests.get(item.get("url"))
        result = result.json()
        result = result.get("result")
        people = People()
        people.name = result.get("properties").get("name")
        people.height = result.get("properties").get("height")
        people.mass = result.get("properties").get("mass")
        people.hair_color = result.get("properties").get("hair_color")
        people.skin_color = result.get("properties").get("skin_color")
        people.eye_color = result.get("properties").get("eye_color")
        people.birth_year = result.get("properties").get("birth_year")
        people.gender = result.get("properties").get("hair_color")
        db.session.add(people)

    try:
        db.session.commit()
        return jsonify("populando listo"), 200
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify("error"), 500

    



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

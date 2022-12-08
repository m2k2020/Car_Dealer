from flask import Flask, abort, jsonify, request
from models import setup_db, Car, db
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    @app.get("/")
    def index():
        cars = db.session.query(Car).filter(Car.owner == None).all()
        all_cars = [car.format() for car in cars]

        if cars is None:
            abort(404)
        return jsonify({"success": True, "cars": all_cars, "total_cars": len(cars)})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "not found"}), 404

    return app

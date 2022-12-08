from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()


def setup_db(app):
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://mhbaando@localhost:5432/dealer_db"
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


# car model
class Car(db.Model):
    __tablename__ = "car"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text(), nullable=False)
    model = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    owner = db.relationship("Sales", backref="car", lazy=True)

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "year": self.year,
            "owner": self.owner,
        }


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False, unique=True)
    owned_car = db.relationship("Sales", backref="customer", lazy=True)


class Sales(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    sell_date = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

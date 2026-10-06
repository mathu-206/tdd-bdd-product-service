"""Models for Product"""
import logging
from decimal import Decimal
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Category(Enum):
    """Product categories"""

    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5


class Product(db.Model):
    """Represents a Product"""

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(
        db.Enum(Category), nullable=False, server_default=Category.UNKNOWN.name
    )

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Product in the database"""
        logger.info("Creating %s", self.name)
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:  # pylint: disable=broad-except
            db.session.rollback()
            raise DataValidationError(e) from e

    def update(self):
        """Updates a Product in the database"""
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:  # pylint: disable=broad-except
            db.session.rollback()
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Product from the database"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:  # pylint: disable=broad-except
            db.session.rollback()
            raise DataValidationError(e) from e

    def serialize(self) -> dict:
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data: dict):
        """Deserializes a Product from a dictionary"""
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = Decimal(str(data["price"]))
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
            self.category = getattr(Category, data["category"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid product: missing " + error.args[0]
            ) from error
        except (TypeError, ArithmeticError) as error:
            raise DataValidationError(
                "Invalid product: bad data - " + str(error)
            ) from error
        return self

    @classmethod
    def all(cls):
        """Returns all of the Products"""
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Product by its ID"""
        return db.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name"""
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_price(cls, price):
        """Returns all Products with the given price"""
        return cls.query.filter(cls.price == Decimal(str(price).strip(' "')))

    @classmethod
    def find_by_availability(cls, available: bool = True):
        """Returns all Products by their availability"""
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_category(cls, category: Category = Category.UNKNOWN):
        """Returns all Products by their Category"""
        return cls.query.filter(cls.category == category)

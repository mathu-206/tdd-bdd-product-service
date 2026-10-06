"""Configuration. Defaults to a local SQLite file so no database server is needed."""
import os

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///products.db")
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

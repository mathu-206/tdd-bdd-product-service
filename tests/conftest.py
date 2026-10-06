"""Use a separate SQLite file for tests (must run before `service` is imported)"""
import os

os.environ.setdefault("DATABASE_URI", "sqlite:///test_products.db")

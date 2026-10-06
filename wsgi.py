"""Run the service: python wsgi.py  (listens on http://localhost:8080)"""
from service import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

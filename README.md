# Product Service: TDD and BDD (Python)

Flask + SQLAlchemy REST service with pytest unit/route tests and Behave (Selenium) BDD tests.

## Setup
```bash
python -m venv venv && source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Uses a local SQLite file by default (set `DATABASE_URI` to use another database).

## Run unit and route tests (Tasks 1-4)
```bash
pytest -v
```

## Run BDD tests (Tasks 5-7)
Terminal 1 (service):
```bash
python wsgi.py
```
Terminal 2 (needs Chrome installed):
```bash
behave
```

## Where each task lives
| Task | File |
|---|---|
| 1 | tests/factories.py |
| 2.1-2.7 | tests/test_models.py |
| 3.1-3.7 | tests/test_routes.py |
| 4.1-4.4 | service/routes.py |
| 5 | features/steps/load_steps.py |
| 6.1-6.7 | features/products.feature |
| 7.1-7.4 | features/steps/web_steps.py |

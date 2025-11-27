## Canteen Reservations API 
Levi9 "5 dana u oblacima 2025" Challenge – Canteen Reservation System
Backend solution for student meal reservations in university canteens.
Includes Students, Canteens, Reservations, and capacity/status logic.

## Technologies
```
Python 3.10+
FastAPI 0.110.0
Uvicorn 0.30.0
Pydantic 2.6.1
pip (package manager)
```

## Project Structure
```
app/
├── routers/
│ ├── students.py
│ ├── canteens.py
│ └── reservations.py
├── database.py
├── models.py
├── utils.py
└── main.py
requirements.txt
README.md
```
## Environment Setup

1. Clone the repository
```
git clone <URL>
cd <repo-folder>
```
2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Build Instructions

No additional build process is required. 
Installing dependencies is considered a build process:
pip install -r requirements.txt

## Running the application
```
Start the FastAPI server:
uvicorn app.main:app --reload --port 8000 
- or any other port of choice, e.g. --port 8080
```

Application will be available at:
```
http://localhost:8000
The API specification will be available at: http://localhost:8000/docs
```

## Postman Public Test Instructions
```
- the application must be running
- the database must be empty before each test run
- import the provided Postman collection and environment files
- in Postman Runner, select "Run manually"
- do not change the order of tests
```
## Running Unit Tests
No unit tests

## Notes
The application uses an in-memory database, so data resets on every restart  
This is required for the official test scenarios to pass


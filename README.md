# Student Database Management API

## Project Overview

The Student CRUD API is a Python backend application developed using FastAPI and SQLite to manage student records. This project was created as part of the Python Backend Development internship assignment at EWB Edu Tech Pvt. Ltd.

## Features

- Create new student records
- Retrieve all student records
- Search students by name or course
- Retrieve a student by ID
- Update student details
- Delete student records
- Validate email addresses
- Prevent duplicate email addresses
- Handle missing student records
- Store records persistently using SQLite

## Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- Swagger UI

## Project Structure

```text
students-crud-api/
├── main.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

- Python 3.10 or later
- Visual Studio Code or another code editor
- A web browser

## Installation and Setup

### 1. Open the project folder

Open the `students-crud-api` folder in your terminal.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m uvicorn main:app --reload
```

The application will run at:

`http://127.0.0.1:8000`

## API Documentation

Open the following URL in your browser to view and test the API:

`http://127.0.0.1:8000/docs`

FastAPI provides interactive documentation where you can execute requests and view responses.

## API Endpoints

| HTTP Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve and filter students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| PUT | `/students/{student_id}` | Update student details |
| DELETE | `/students/{student_id}` | Delete a student |

## Filtering Students

Students can be filtered by name or course.

Example requests:

```text
GET /students?name=Lahari&limit=100
GET /students?course=CSE-AI&limit=100
```

The `limit` parameter controls the maximum number of records returned.

## Example: Create a Student

Send a POST request to `/students` with the following JSON body:

```json
{
  "name": "Demo Student",
  "date_of_birth": "2005-09-20",
  "email": "demo.student@example.com",
  "phone": "9000000000",
  "course": "CSE-AI"
}
```

Use fictional student information when testing.

## Database

The application uses SQLite to store student records. The students table is created automatically when the application starts.

Student records persist across application restarts.

The database contains the following fields:

- `id` — Unique student ID
- `name` — Student name
- `date_of_birth` — Student date of birth
- `email` — Student email address
- `phone` — Student phone number
- `course` — Student course

## Error Handling

The API handles common errors:

- **400 Bad Request:** Invalid update request or limit
- **404 Not Found:** Student record does not exist
- **409 Conflict:** Email address already exists
- **422 Unprocessable Entity:** Invalid request data

## Future Improvements

- Add automated unit tests
- Improve date-of-birth validation
- Add optional AI-powered student queries using Ollama

## Author

Developed as a Python Backend Development internship project at EWB Edu Tech Pvt. Ltd.
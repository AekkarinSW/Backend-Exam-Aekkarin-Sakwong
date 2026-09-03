# School REST API

This Django REST Framework project implements the school, classroom, teacher, and student APIs described in `api_exam.md`.

## Setup

```bash
cd 4_rest_api
python -m venv .venv
```

Activate the virtual environment:

```bat
.venv\Scripts\activate
```

For macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies and prepare the database:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

The API requires authentication. Basic authentication and Django session authentication are enabled.

## Endpoints

- `/api/v1/schools/`
- `/api/v1/classrooms/`
- `/api/v1/teachers/`
- `/api/v1/students/`

Each endpoint supports create, list, detail, update, and delete operations.

## Filters

- School: `name`
- Classroom: `school`
- Teacher: `school`, `classroom`, `firstname`, `last_name`, `gender`
- Student: `school`, `classroom`, `firstname`, `last_name`, `gender`

Name filters are case-insensitive and support partial matches. The API also accepts `first_name` and `lastname` as aliases.

## Tests

```bash
python manage.py test
```

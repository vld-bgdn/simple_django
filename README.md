# Simple Django store app
The application includes:
- Product catalog with categories
- Admin interface for store management
# Getting Started
## Prerequisites
- Python 3.11 or higher
- Poetry (Python dependency management)
## Installation
- Clone the repository:
```
git clone https://github.com/vld-bgdn/simple_django.git
cd django_store
```
- Install dependencies using Poetry:
- Install Poetry if you don't have it already
```
curl -sSL https://install.python-poetry.org | python3 -
```
- Install project dependencies
```
poetry install
```
- Activate the virtual environment:
```
poetry shell
```
- Set up the database:
```
python manage.py migrate
```
- Create a superuser:
```
python manage.py createsuperuser
```
- Start the Django server:
```
python manage.py runserver
```
- Visit http://127.0.0.1:8000/ in your browser to see the application.

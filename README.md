## Cat Charity Fund

**Stack:**
* Python 3.9
* FastAPI 0.78
* SQLAlchemy 1.4
* SQLite

### DESCRIPTION

It's a project that helps you make someone (like a cat) happier.

### INSTALL

Clone the project:
```
git clone https://github.com/AndreyVnk/cat_charity_fund.git && cd cat_charity_fund/
```
Install virtual environment:
```
python3.9 -m venv venv
```
Activate virtual environment:
```
source venv/bin/activate for Linux
source venv/Scripts/ctivate for Windows
```
Upgrade pip:
```
python3 -m pip install --upgrade pip
```
Install requirements:
```
pip install -r requirements.txt
```
Create .env file or change app.core.config parameters:
```
touch .env
```
Fill the .env file:
```
APP_TITLE=App_title
DESCRIPTION=Description
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=Secret
FIRST_SUPERUSER_EMAIL=login@email.com
FIRST_SUPERUSER_PASSWORD=password
```

### START

Run project:
```
uvicorn app.main:app --reload
```
The project will be available at http://127.0.0.0:8000/ .

Documentation is available at: 
* Swagger: http://127.0.0.0:8000/docs
* ReDoc: http://127.0.0.0:8000/redoc

**Author:** AndreyVnk
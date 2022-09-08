# MK-Tech
## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/joy1954islam/MK-Tech.git
```

Create Virtual Env and Install the requirements:

```bash
cd MK-Tech
python3 -m virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

* Then Makemigrations Command
```python manage.py makemigrations```


* Migrate Command
```python manage.py migrate```

* Server Run Command
```python manage.py runserver```

* load db json data
``` python manage.py loaddata db.json```

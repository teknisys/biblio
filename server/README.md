# BIBLIO SERVER

[README WIP]

# Installation

```
pip install -r requirements.txt
```

# Running

```
uvicorn main:app --reload
```

To fill in fake data into the DB, first run the app and then:

```
python3 autoPopulateDB.py
```

# Docs

Automatic documentation provided by SwaggerUI and ReDoc

```
Swagger docs: 127.0.0.1/docs

ReDoc: 127.0.0.1/redoc
```

# Docker

```
docker build -t adi:biblio .
```

```
docker run -d --name biblio -p 8000:8000 adi:biblio
```

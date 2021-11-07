### Notezilla API

## Table of contents

-   [General info](#general-info)
-   [Features](#features)
-   [API Endpoints](#api-endpoints)
-   [Technologies](#technologies)
-   [Setup](#setup)

## General info<a name="general-info"></a>

Notezilla API is a REST API built with Flask & SQLAlchemy to operate CRUD operation on a database. The different routes are described below in the API Endpoint section.

## Features<a name="features"></a>

-   Allow user to fetch notes
-   Allow user to fetch singular note
-   Allow user to post note
-   Allow user to delete note
-   Allow user to update note

## API Endpoints<a name="api-endpoints"></a>

After running the server, consult Documentation at :

> https://flask-notezilla.herokuapp.com/

-   notes CRUD

    -   Return JSON with all notes
    -   Return JSON with singular note
    -   Add new note
    -   Update existing note
    -   Delete existing note

Database schema:

![DB Screenshot](https://templars.guru/app/github/notezilla_api/Notes%20DB.png)

## Technologies<a name="technologies"></a>

Project is created with: Python / Flask

## Setup<a name="setup"></a>

### Import project

```
$ git clone https://github.com/antoineratat/api_notezilla.git
$ py -3 -m venv venv
$ venv\Script\Activate
$ cd api_note
$ pip install -r requirements.txt
```

### Create Environnement Variable

```
$ code config.json

{
	"SECRET_KEY": "secret_key",
	"DATABASE_URL": "sqlite:///dbname.db",
	"JWT_SECRET_KEY": "jwt_key"
}

```

### Initialize Database

```
$ venv\Script\Activate
$ python
$ from run import db
$ db.create_all()
$ exit()
```

### Run project

```
$ python run.py
```

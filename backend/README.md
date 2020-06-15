# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

<!-- 
JWT for MANAGER
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTE2OTg2MTc5NzcxMDM0Mjc5ODkiLCJhdWQiOlsiY29mZmVlLWFwaSIsImh0dHBzOi8vZGV2LWZjMzR5OWxxLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTIxNzg5ODAsImV4cCI6MTU5MjE4NjE4MCwiYXpwIjoiRTdEMm5rNUt0Nnp3cmFFU1BtRlAxMmZRSUpxdGFnQWIiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.G9pLu06RgeSaCHMjHdoBs7ok6z7k24pVDG1oWyemJ-nL_FpkSR889e1FFJhCSqo41_h2PUeevhItD1lFgIzlahj9k8kYtEB1uDgJb5-PSx5iRojUuVOf9vt6dJ1O6L1Ekzwq5CxplJubKhOH2mXO0J821fVrlIH0WJLp29th7GcIx9KD1UZlPzRma5jHOZc16frDNC9CB614rwQNDu4el6QLylUCskYSiKEsRWIfhmX6sEyA5DGOXnGZg4fRMQJnzf2V0-uSfIDuySu6FpJjqWTqzoICqO4kZSPyFSSTf28CIGskkF4B6bxn5aitpg02A1kVaJf_TC5bTZmjh3Q97Q
-->

<!-- 
JWT for BARISTA
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTcwODg0NzY1NDYyODExMDQ4MDIiLCJhdWQiOlsiY29mZmVlLWFwaSIsImh0dHBzOi8vZGV2LWZjMzR5OWxxLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTIxNzkwMDUsImV4cCI6MTU5MjE4NjIwNSwiYXpwIjoiRTdEMm5rNUt0Nnp3cmFFU1BtRlAxMmZRSUpxdGFnQWIiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.sMSK8lHS6h7KhI2vARs0VwRBCOUaZ9qBrTKk5B3GxTFm5Xbgo5X8pHxjlcigq6XYUVdW4bNTdxH4ZifWjAMvzYo90HxG5VRiQEU3V9ZKgVeE-WAXZ-Nly4NQXmPQbzqSglMcSOJH2mnQgdMsOs096w_MP3bjiMY9oUComCgGwA7Tz-v4e1DaIgew92wTRycR0juB3oUpVOZs0MnqUe9cm8zUoR79wAY6_FBHK6G0IjmLWtr20C-dvid7gMTpbEZF8QyjtzPRUMlSi5T0srOa0Eb5kkh_yY9HTFv47poVGTM_FTJa-kDNUlUGQZPlI_re3iJvVERmROlMk9U53MMtIg
-->
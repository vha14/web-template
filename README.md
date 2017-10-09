## What is it?

A docker-friendly web project template with the following pieces:

- ReactJS client-side Typescript (`client-ts` folder) based on Create React App template.
- Multi-tier server architecture with:
    - NGINX reverse proxy (`nginx` folder).
    - Flask-based application server with Python 3.6 or later (`server` folder).
    - Postgres database (`db` folder).
- Unit test management with `tox`.
- Code linting with Flake8 for Python, and Tslint for Typescript.
    
This is based on Michael Herman's http://testdriven.io/.

In addition, the following are supported:

- Blueprints for component-based Flask development.
- Database migration with flask-migrate.
- User password encryption with flask-bcrypt.
- Token-based user authentication with pyjwt (Json Web Token).

## Why Python? 

The application server can be written in other languages but Python was 
picked with the assumption that we also want to do ML/NLP which is where
Python dominates. We aim to minimize context switch.

Flask was picked since it's minimalist but can be extended easily.

    
## Quick start for Mac OS users with Docker for Mac

- Setup Docker for Mac (note: this is different from Docker toolbox for Mac).
- Set the server URL for the ReactJS app: 
    - bash: `export REACT_APP_USERS_SERVICE_URL=http://localhost:8080`.
    - fish: `set -x REACT_APP_USERS_SERVICE_URL http://localhost:8080`.
- Start all four containers (client, nginx, server, and postgres) with a single command: `docker-compose up -d`.
- Check that the webapp is up and running at http://localhost:8080

## Quick start for local setup on Mac OS

This section is for fish shell users. Bash users can easily extrapolate. This setup does not include nginx.

- Ensure Python 3.6 or later, Node, and Postgres are installed.
- In the main directory, create and activate a virtualenv, and install the dependencies. For example (in fish shell):
    - `python3 -m venv venv`.
    - `source ./venv/bin/activate.fish`.
    - `pip install -r requirements.txt`.
- Setup the postgres database. In the activated virtualenv, run:
    - `source ./scripts/setup-local-dev.fish`. This sets up the postgres-related environment variables.
    - `python manage.py recreate_db`.
    - `python manage.py seed_db`.
- Test the backend server (all tests should pass):
    - `python manage.py test`.
    - Use of tox to manage code style in addition to tests is encouraged:
        - `pip install tox`. This can be done outside of the virtualenv.
        - `tox`. Tox checks for code style issues using flake8, and runs all the tests.
- Start the server:
    - `python manage.py runserver`. This server listens to port 5000 by default.
- Change to `client-ts` directory and start the webapp:
    - `cd client-ts`.
    - `npm install`.
    - `set -x REACT_APP_USERS_SERVICE_URL http://localhost:5000`.
    - `npm start`. This should start the webapp at http://localhost:3000.

## Deploying to a single EC2 machine

- Create a EC2 machine called 'sandbox' that exposes port 80: 
    - `docker-machine create --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-open-port 80 sandbox`.
- Once done, set it to be the active host: 
    - bash: `eval $(docker-machine env sandbox)` 
    - fish: `eval (docker-machine env sandbox)` 
    - Note the IP address with: `docker-machine ip sandbox`.
- Set the server URL for the ReactJS app: 
    - bash: `export REACT_APP_USERS_SERVICE_URL=http://EC2-Machine-IP`.
    - fish: `set -x REACT_APP_USERS_SERVICE_URL http://EC2-Machine-IP`.
- Start all four containers: `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`.
- Check that the webapp is up and running at http://EC2-Machine-IP.

## Optional: Running tests in docker

- Create and seed the users database: 
    - `docker-compose run users-service python manage.py recreate_db`.
    - `docker-compose run users-service python manage.py seed_db`.
- Make sure the tests pass:
    - `docker-compose run users-service python manage.py test`.
- Run tests with coverage:
    - `docker-compose run users-service python manage.py cov`.

## TODOS

- Add continuous integration (Travis).
- Frontend: redux.
- Frontend: styled-components.
- Frontend: splitting/hot loading
- Frontend: e2e testing (see for example:http://testdriven.io/part-four-intro/).
- Backend: scale to multiple EC2 machines (using Kubernetes?).
- Backend: redis caching.
- Backend: comprehensive authentication solution (oauth with Google/Facebook, forgot password, etc.).
Look into flask authentication extensions (e.g. flask-login).
- Backend: elasticsearch (look into searchkit).
- Backend: swagger (http://testdriven.io/part-four-swagger-setup/).

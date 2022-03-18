# fastapi_todos

### Prerequisites

- [Python](https://www.python.org/)
- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)

### Installation instructions

1. After downloading the project create and fill out the local settings file:

    ```
    cp env.local.example .env
    ```

2. Configure your local database by filling out `DJANGO_DATABASE_URL` setting in `.env` file. Make sure the username, password, and database name match the environment variables in docker-compose.yml

3. Configure IPstack token by filling out `IP_STACK_ACCESS_KEY` setting in `.env` file.

4. After downloading the project and filling out the env file aggregate the container:

    ```
    docker-compose up
    ```

5. Run test command to make sure everything is in order:

        docker-compose run web ./manage.py test

6. Start the development server:

        docker-compose up
        or
        docker-compose run web ./manage.py runserver

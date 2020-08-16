# mathsoc-bot

# secrets setup

- Create a copy of `.env.example` as `.env` and fill in the secrets
- `EMAIL_KEY` and `TOKEN_SECRET` can be generated using `poetry run gen_tokens`

# poetry setup

https://github.com/sdispater/poetry

`poetry install`

# running the bot using docker compose

`docker-compose up -d`

## After making changes to the db schema, you should run

``` shell
poetry run alembic revision --autogenerate -m "<description of schema change>"
```

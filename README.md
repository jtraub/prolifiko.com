# Development

# Getting Started

```sh
$> mkvirtualenv prolifiko
$> pip install -r requirements.common.txt
```

Use `requirements.common.txt` to install dependencies. This keeps `psycopg2` separate
so you don't have to have Postgres installed to work on the project.

Update dependencies with:

    $> pip install -r requirements.common.txt --upgrade
    $> pip freeze > requirements.common.txt

FROM python:slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN set -eux; \
    pip install poetry; \
    poetry install --no-dev --no-root

COPY . .

ENTRYPOINT [ "poetry", "run", "web2preview" ]
CMD [ "example.com" ]
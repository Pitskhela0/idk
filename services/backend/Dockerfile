# == Base builder ==
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 PYTHONPATH=.

WORKDIR /services

COPY poetry.lock pyproject.toml /services/
RUN pip install -U pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY ./apps /services/apps

# == Development ==
FROM builder AS dev

RUN poetry install --with dev --no-root

RUN useradd -m -d /services -s /bin/bash app && \
    chown -R app:app /services

USER app


# == Production ==
FROM builder AS production

RUN poetry install --only main --no-root

RUN useradd -m -d /services -s /bin/bash app && \
    chown -R app:app /services

USER app

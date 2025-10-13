# == Base builder ==
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 PYTHONPATH=.

WORKDIR /tennant-middleware

COPY poetry.lock pyproject.toml /tennant-middleware/
RUN pip install -U pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY ./src /tennant-middleware/src

# == Development ==
FROM builder AS dev

RUN poetry install --with dev --no-root

RUN useradd -m -d /tennant-middleware -s /bin/bash app && \
    chown -R app:app /tennant-middleware

USER app


# == Production ==
FROM builder AS production

RUN poetry install --only main --no-root

RUN useradd -m -d /tennant-middleware -s /bin/bash app && \
    chown -R app:app /tennant-middleware

USER app

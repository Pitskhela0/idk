FROM python:3.11.4

ENV PYTHONUNBUFFERED=1 PYTHONPATH=.

WORKDIR /tennant-middleware

COPY poetry.lock pyproject.toml /tennant-middleware/
RUN pip install -U pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

ARG POETRY_INSTALL_DEV=true
RUN if [ "$POETRY_INSTALL_DEV" = "true" ]; then poetry install --with dev ; else poetry install --only main ; fi

COPY ./src /tennant-middleware/src

RUN useradd -m -d /tennant-middleware -s /bin/bash app && \
    chown -R app:app /tennant-middleware

USER app

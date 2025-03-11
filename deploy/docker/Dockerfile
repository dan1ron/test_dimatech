FROM python:3.12-slim as base

ENV PYTHONBUFFERED 1

FROM base as python-deps

ENV PIPENV_VENV_IN_PROJECT 1
ENV PIP_DEFAULT_TIMEOUT=999

RUN pip install --no-cache-dir --upgrade pip pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync --dev --verbose

FROM base as runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /sources

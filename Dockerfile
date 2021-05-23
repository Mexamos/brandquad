FROM python:3.9.5 as requirements-builder

RUN mkdir build/
WORKDIR /build/

RUN pip install poetry

COPY pyproject.toml poetry.lock /build/

RUN poetry export --with-credentials --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.9.5

RUN mkdir code/
WORKDIR /code/

COPY --from=requirements-builder /build/requirements.txt /code/requirements.txt

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN pip install -r requirements.txt

COPY . /code/

FROM python:3.11.6-alpine3.18

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .

RUN python -m venv /.pyvenv && \
    /.pyvenv/bin/pip install --upgrade pip && \
    /.pyvenv/bin/pip install -r requirements.txt

ENV PATH="/.pyvenv/bin:$PATH"

COPY . .

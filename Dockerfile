# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install -U pip && \
    python -m pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "execute.py" ]
CMD [ "cca" ]

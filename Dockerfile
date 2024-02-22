FROM python:3.11
WORKDIR /app
COPY . /app
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install
CMD ["poetry", "run", "python", "app.py"]

FROM python:3.11
WORKDIR /app
COPY . /app
RUN python3 -m pip install poetry
RUN poetry install
CMD ["poetry", "run", "python", "src/app.py"]

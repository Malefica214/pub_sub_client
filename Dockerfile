FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY pyproject.toml /code/pyproject.toml

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY /app /code/app

CMD ["uvicorn", "app.main_pub:app", "--host", "0.0.0.0", "--port", "8000"]

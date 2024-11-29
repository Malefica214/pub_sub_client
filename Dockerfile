FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY pyproject.toml /code/pyproject.toml

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY /app /code/app


CMD ["fastapi", "run", "app/main_pub.py", "--port", "8000"]
CMD ["fastapi", "run", "app/main_sub.py", "--port", "9100"]
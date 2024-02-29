 FROM python:slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /code/
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

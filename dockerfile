FROM python:latest

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -u pip
RUN pip install -r requirements.txt

COPY . /code/
EXPOSE 8000

CMD ["gunicorn", "A.wsgi", "8000"]


FROM python:3.12

WORKDIR /app

COPY ./src /app/app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--reload"]
FROM python:latest

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --upgrade -r requirements.txt

COPY . /app

CMD [ "python", "./src/main.py"]

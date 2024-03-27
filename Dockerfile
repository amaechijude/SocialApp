FROM python:3.11.4-slim-bullseye

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

COPY build.sh /app

RUN chmod +x build.sh
RUN ./build.sh


ENTRYPOINT [ "gunicorn", "core.wsgi", "-b", "0.0.0.0:8000"]
#EXPOSE 8000
#CMD [ "Python3", "manage.py", "runserver" ]
FROM Python:3.111.4-slim-bullseye

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY build.sh .

RUN chmod +x build.sh
RUN ./build.sh


ENTRYPOINT [ "gunicorn", "core.wsgi" ]
#EXPOSE 8000
#CMD [ "Python3", "manage.py", "runserver" ]
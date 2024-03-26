FROM Python3.10

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY build.sh .

RUN chmod +x build.sh
RUN build.sh

EXPOSE 8000

CMD [ "Python3", "manage.py", "runserver" ]
FROM tnir/mysqlclient

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "STORAGE_TYPE=db", "python", "main.py" ]

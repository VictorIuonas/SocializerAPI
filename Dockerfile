FROM python:3.7

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD flask db upgrade ; flask run --host=0.0.0.0

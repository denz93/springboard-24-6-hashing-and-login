FROM python:3.10.4-slim



RUN mkdir /app
WORKDIR /app
COPY . .

RUN mkdir -p /root/.postgresql && mkdir -p /home/.postgresql
RUN cp ./postgresql/root.crt /root/.postgresql/root.crt
RUN cp ./postgresql/root.crt /home/.postgresql/root.crt

RUN pip install -r requirements.txt
CMD gunicorn -b "0.0.0.0:5000" -w 2 --timeout 0 "run:create_app()"
FROM python:3.6-alpine
COPY . /app
WORKDIR app
RUN pip install config42 python-etcd redis==3.2.1 Werkzeug==0.14.1

ENTRYPOINT ["./shortly.py"]

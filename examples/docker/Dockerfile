FROM python:3
WORKDIR app
COPY . .
RUN pip install config42


ENTRYPOINT ["python", "/app/app.py"]
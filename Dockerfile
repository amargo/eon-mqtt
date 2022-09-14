FROM python:alpine

COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app/eon.py"]
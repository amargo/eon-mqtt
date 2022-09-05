FROM python:alpine


RUN apk --update --no-cache add bash
RUN pip install --upgrade pip paho-mqtt bs4 requests
RUN mkdir -vp /eon/log
RUN echo '0 5 * * * /usr/bin/python3 /eon/read_eon_180_280.py >> /eon/log/eon.log 2>&1' >/etc/periodic/daily/eon
RUN chmod -v +x /etc/periodic/daily/eon

COPY read_eon_180_280.py /eon

WORKDIR /eon

VOLUME ['/eon/log']

ENTRYPOINT ["/usr/sbin/crond" , "-f"]

# docker build -t eon-mqtt .
# docker run -dit --name eon-mqtt -v $PWD/mqtt.ini:/eon/mqtt.ini:ro -v $PWD/eon.ini:/eon/eon.ini:ro -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro eon-mqtt

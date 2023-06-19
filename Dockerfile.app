FROM ubuntu:latest

WORKDIR /artwork

COPY requirements.txt .
COPY setup.py .

RUN apt-get -y update \
    && apt-get install -y cron nano python3 python3-pip \
    && touch /var/log/cron.log \
    && pip3 install -r requirements.txt

COPY /artwork /artwork/artwork
RUN pip3 install .
COPY crontab /etc/cron.d/cjob
RUN chmod 0644 /etc/cron.d/cjob
RUN chmod 0644 ./artwork/start.sh && chmod +x ./artwork/start.sh && chmod +x ./artwork/job.sh

CMD ["/artwork/artwork/start.sh"]
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y inkscape python3 python3-pip && \
    pip3 install watchdog

WORKDIR /app
COPY watcher/ /app/

CMD ["python3", "watcher.py"]

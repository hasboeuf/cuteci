FROM ubuntu:18.04

RUN apt-get update && apt-get install --yes --no-install-recommends --quiet \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    xvfb \
    libfontconfig \
    libdbus-1-3

ENV PYTHONUNBUFFERED=1

WORKDIR /root/workspace

ENTRYPOINT ["/bin/bash"]

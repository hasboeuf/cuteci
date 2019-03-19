FROM ubuntu:18.04

RUN apt-get update && apt-get install --yes \
    python3 \
    python3-pip \
    xvfb \
    libfontconfig

WORKDIR /root/workspace

COPY data $WORKDIR

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/bash"]

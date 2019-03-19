FROM ubuntu:18.04

RUN apt-get update && apt-get install --yes \
    python3 \
    python3-pip \
    xvfb \
    libfontconfig

WORKDIR /root/workspace

ENTRYPOINT ["/bin/bash"]

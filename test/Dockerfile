FROM ubuntu:18.04

RUN apt-get update && apt-get install --yes --no-install-recommends --quiet \
    python3 \
    xvfb \
    libfontconfig \
    libdbus-1-3

WORKDIR /root/workspace

ENTRYPOINT ["/bin/bash"]

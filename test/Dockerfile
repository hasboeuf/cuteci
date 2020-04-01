FROM ubuntu:18.04

RUN apt-get update && apt-get install --yes --no-install-recommends --quiet \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    xvfb \
    libfontconfig \
    libdbus-1-3 \
    # For some reason Qt installer 5.12 requires:
    libxrender1 \
    libxkbcommon-x11-0

ENV PYTHONUNBUFFERED=1

# Create worker user with same permissions than the caller of `build` script.
ARG UID=1000
ARG GID=1000
ENV USER worker
RUN groupadd --gid $GID worker
RUN useradd --create-home --gid $GID --uid $UID $USER --shell /bin/bash \
    && echo "$USER:worker" | chpasswd
WORKDIR /home/$USER
ENV PATH="/home/worker/.local/bin:${PATH}"
USER worker

ENTRYPOINT ["/bin/bash"]

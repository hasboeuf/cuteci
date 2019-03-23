# CuteCI

[![Build Status](https://travis-ci.org/hasboeuf/cuteci.svg?branch=master)](https://travis-ci.org/hasboeuf/cuteci)

CuteCI is a simple script allowing you to install Qt in headless mode.
Qt installers are using Qt Installer Framework which provides scripting ability.

## Requirements

* `Python3`

`deploy_qt` is in Python but has only been tested on Ubuntu (+docker).

`deploy_qt` has is tested with Qt installer `5.9.7` `5.10.1` `5.11.3` `5.12.2`.

## Principle

`deploy_qt` does few things:

* Download Qt installer if you pass an url
* Make installer executable
* Install Qt with desired packages in the directory you choose

`deploy_qt` can also only lists packages available in the installer.

## Usage

Common options:

* `--installer` (required): path or url to Qt installer. If url, choose an official one from `download.qt.io/official_releases/qt/`, this is because `md5sums.txt` is retrieved implicitely from it.
* `--ui`: if set, Qt installer UI is shown (useful for debugging).
* `--rm`: if set, Qt installer is removed at the end.

### List packages

```bash
./deploy_qt
    --installer <path or official url> \
    [--ui] [--rm] \
    list
```

Will output:

```
===LIST OF PACKAGES===
qt    Qt
qt.qt5.5122    Qt 5.12.2
qt.tools    Developer and Designer Tools
qt.installer.changelog    Qt Installer Changelog
qt.license.lgpl    Qt License LGPL
qt.license.thirdparty    Qt 3rd Party Licenses
qt.license.python    Python Software Foundation License Version 2
qt.license.gplv3except    License GPL3-EXCEPT
qt.qt5.5122.gcc_64    Desktop gcc 64-bit
qt.qt5.5122.android_x86    Android x86
qt.qt5.5122.android_arm64_v8a    Android ARM64-v8a
qt.qt5.5122.android_armv7    Android ARMv7
...
===END OF PACKAGES===
```

### Install

```bash
./deploy_qt \
    --installer <path or official url> \
    [--ui] [--rm] \
    install \
    --destdir /opt/Qt \
    --packages qt.qt5.5122.gcc_64,qt.qt5.5122.android_x86 \
    [--verbose] [--keep-tools]
```

#### Notes

* `destdir` should not contain a previous Qt installation (unless it has been installed with `deploy_qt`),
  Otherwise installer will complain and script does not handle it.
* If `--keep-tools` is set, QtCreator, Maintenance Tools, samples and doc will be kept,
  but you will not be able to install another version of Qt in `destdir`.

## Docker integration

Here is the sample of a minimalist Dockerfile using `deploy_qt` to install Qt 5.12.2:

```bash
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    libdbus-1-3 \
    xvfb \
    libfontconfig \
    python3 \
    ca-certificates \
    wget

RUN wget https://github.com/hasboeuf/cuteci/raw/1.0.0/deploy_qt && \
    wget https://github.com/hasboeuf/cuteci/raw/1.0.0/install-qt.qs && \
    chmod +x deploy_qt && \
    ./deploy_qt \
        --rm \
        --installer http://download.qt.io/official_releases/qt/5.12/5.12.2/qt-opensource-linux-x64-5.12.2.run \
        install \
        --destdir /opt/Qt \
        --packages qt.qt5.5122.gcc_64 && \
    rm --force deploy_qt install-qt.qs

ENTRYPOINT ["/bin/bash"]
```

## Testing

Covered by docker and Travis CI, have a look to `test` dir if you are curious.

## Code sanity

Coding style is handled by `black` (via `./blackify`).
Static checks are handled by `pylint` (via `./pylintify`).

You must `pip3 install -r requirements/codesanity.txt` to use those scripts.

Note: continuous integration does not check code sanity.

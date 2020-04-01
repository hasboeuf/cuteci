# CuteCI

[![Build Status](https://travis-ci.org/hasboeuf/cuteci.svg?branch=master)](https://travis-ci.org/hasboeuf/cuteci)
[![PyPI version](https://badge.fury.io/py/cuteci.svg)](https://pypi.org/project/cuteci/)
![License](https://img.shields.io/github/license/mashape/apistatus.svg)

CuteCI is a simple tool allowing you to install Qt framework with desired packages in headless mode.
Qt installers are using Qt Installer Framework which provides scripting ability,
CuteCI takes advantage of this.

## Requirements

* `Python3` `pip3`
* `cuteci` is in Python but has only been tested on Ubuntu (+docker).
* `cuteci` is tested with latest patch version of Qt `5.9` `5.12` `5.13`, `5.14` (`5.10` `5.11` are not online anymore).

## Installation

`pip3 install cuteci`

## Principle

`cuteci` does few things:

* Download Qt installer if you pass an url
* Make installer executable
* Install Qt with desired packages in the directory you choose

`cuteci` can also only lists packages available in the installer.

## Usage

Common options:

* `--installer` (required): path or url to Qt installer. If url, choose an official one from `download.qt.io/official_releases/qt/`, this is because `md5sums.txt` is retrieved implicitely from it.
* `--ui`: if set, Qt installer UI is shown (useful for debugging).
* `--rm`: if set, Qt installer is removed at the end.
* `--timeout`: duration in seconds to wait for the operation to be finished.

### List packages

```bash
cuteci \
    --installer <path or official url> \
    [--ui] [--rm] \
    list
```

Will output:

```bash
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
cuteci \
    --installer <path or official url> \
    [--ui] [--rm] \
    install \
    --destdir /opt/Qt \
    --packages qt.qt5.5122.gcc_64,qt.qt5.5122.android_x86 \
    [--verbose] [--keep-tools]
```

#### Notes

* `destdir` should not contain a previous Qt installation (unless it has been installed with `cuteci`),
  otherwise installer will complain and script does not handle it.
* If `--keep-tools` is set, QtCreator, Maintenance Tools, samples and doc will be kept,
  but you will not be able to install another version of Qt in `destdir`.

## Docker integration

Here is the sample of a minimalist Dockerfile using `cuteci` to install Qt 5.12.2:

```bash
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    libdbus-1-3 \
    xvfb \
    libfontconfig \
    python3 \
    python3-pip
    # For some reason Qt installer 5.12 requires:
    libxrender1 \
    libxkbcommon-x11-0

RUN pip3 install cuteci && \
    cuteci \
        --rm \
        --installer http://download.qt.io/official_releases/qt/5.12/5.12.2/qt-opensource-linux-x64-5.12.2.run \
        install \
        --destdir /opt/Qt \
        --packages qt.qt5.5122.gcc_64

ENTRYPOINT ["/bin/bash"]
```

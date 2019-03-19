[![Build Status](https://travis-ci.org/hasboeuf/cuteci.svg?branch=master)](https://travis-ci.org/hasboeuf/cuteci)

# CuteCI

CuteCI is a simple script allowing you to install Qt in headless mode.
Qt installer is using Qt Installer Framework which provides scripting ability.

## Requirements

* `Python3` and `pip3`

`deploy_qt` is in Python but has only been tested on Ubuntu (+docker).

## Principle

`deploy_qt` does few things:
- Download Qt installer if you pass an url
- Make the installer executable
- Install Qt with desired packages in the directory you choose

`deploy_qt` can also only lists packages available in the installer.

## Usage

Common options:
* `--installer`: path or url to Qt installer. If url, choose an official one from `download.qt.io/official_releases/qt/`,
                 this is because `md5sums.txt` is retrieved implicitely from it.
* `--headless`: if set, Qt installer UI does not show up at all.

### List packages

```
./deploy_qt \
    --installer <path or official url> \
    --list-packages \
    [--headless]
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

```
./deploy_qt \
    --installer <path or official url> \
    --destdir /opt/ \
    --packages qt.qt5.5122.gcc_64,qt.qt5.5122.android_x86 \
    [--headless]
```

#### Notes

* `destdir` should not contain a previous Qt installation,
  otherwise installer will complain and script does not handle it.
* If Qt `X.Y.Z` is going to be installed, `deploy_qt` will use `scripts/install-X.Y.qs`.
  Currently only script for `5.12` exists, so it will fallback on it.
  Feel free to push a PR to cover more versions.

### Test

Covered by docker and Travis CI, have a look to `test` dir if you're curious.

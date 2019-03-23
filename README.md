[![Build Status](https://travis-ci.org/hasboeuf/cuteci.svg?branch=master)](https://travis-ci.org/hasboeuf/cuteci)

# CuteCI

CuteCI is a simple script allowing you to install Qt in headless mode.
Qt installers are using Qt Installer Framework which provides scripting ability.

## Requirements

* `Python3`

`deploy_qt` is in Python but has only been tested on Ubuntu (+docker).

## Principle

`deploy_qt` does few things:
- Download Qt installer if you pass an url
- Make installer executable
- Install Qt with desired packages in the directory you choose

`deploy_qt` can also only lists packages available in the installer.

## Usage

Common options:
* `--installer` (required): path or url to Qt installer. If url, choose an official one from `download.qt.io/official_releases/qt/`, this is because `md5sums.txt` is retrieved implicitely from it.
* `--headless`: if set, Qt installer UI does not show up at all.
* `--cleanup`: if set, Qt installer is removed at the end.

### List packages

```
./deploy_qt list \
    --installer <path or official url> \
    [--headless] [--cleanup]
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
./deploy_qt install \
    --installer <path or official url> \
    --destdir /opt/Qt \
    --packages qt.qt5.5122.gcc_64,qt.qt5.5122.android_x86 \
    [--headless] [--cleanup]
```

#### Notes

* `destdir` should not contain a previous Qt installation,
  otherwise installer will complain and script does not handle it.
* If Qt `X.Y.Z` is going to be installed, `deploy_qt` will use `install-X.Y.qs`.
  Currently only script for `5.12` exists, so it will fallback on it by default.
  Feel free to push a PR to cover more versions.

### Testing

Covered by docker and Travis CI, have a look to `test` dir if you are curious.

### Code sanity

Coding style is handled by `black` (via `./blackify`).
Static checks are handled by `pylint` (via `./pylintify`).

You must `pip3 install -r requirements/codesanity.txt` to use those scripts.

Note: continuous integration does not check code sanity.

#!/usr/bin/env python3

"""
Deploy Qt
"""

import sys
import os
import stat
import shutil
import argparse
from urllib.request import urlopen
import hashlib
import re
import subprocess

import cuteci

WORKING_DIR = os.getcwd()
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MD5SUMS_FILENAME = "md5sums.txt"
DEFAULT_INSTALL_SCRIPT = os.path.join(CURRENT_DIR, "install-qt.qs")
INSTALL_TIMEOUT = 120  # 2 minutes

EXIT_OK = 0
EXIT_ERROR = 1


def _download_qt(qt_url):
    filename = qt_url[qt_url.rfind("/") + 1 :]
    md5sums_url = qt_url[: qt_url.rfind("/")] + "/" + MD5SUMS_FILENAME

    qt_installer = os.path.join(WORKING_DIR, filename)

    # Download Qt
    print("Download Qt", qt_url)

    def print_progress(size, length):
        # Print progress every 5%
        if not hasattr(print_progress, "prev"):
            print_progress.prev = -1  # Then 0% is printed
        percent = int(size * 100 / length)
        progress = percent - percent % 5
        if progress != print_progress.prev:
            print("\rFetched {}%".format(progress), end="")
            print_progress.prev = progress

    hash_md5 = hashlib.md5()
    with open(qt_installer, "wb") as qt_installer_file:
        req = urlopen(qt_url)
        length = int(req.getheader("content-length", 1500000000))
        size = 0
        while True:
            chunk = req.read(4096)
            if not chunk:
                break
            size += len(chunk)
            hash_md5.update(chunk)
            qt_installer_file.write(chunk)
            print_progress(size, length)

    # Download md5sums and check
    print()
    print("Download md5sums", md5sums_url)
    response = urlopen(md5sums_url)
    print("Check md5sums")
    if hash_md5.hexdigest() not in str(response.read()):
        print("Checksums do not match")
        return EXIT_ERROR

    print("Download OK", qt_installer)
    return qt_installer


def _get_version(qt_installer):
    # qt-opensource-windows-x86-5.12.2.exe
    # qt-opensource-mac-x64-5.12.2.dmg
    # qt-opensource-linux-x64-5.12.2.run
    basename = os.path.basename(qt_installer)
    res = re.search(r"-(\d+\.\d+.\d+)\.", basename)
    return res.group(1)


def _get_major_minor_ver(qt_installer):
    return ".".join(_get_version(qt_installer).split(".")[:1])


def _get_install_script(version):
    path = os.path.join(CURRENT_DIR, "install-qt-{}.qs".format(version))
    if not os.path.exists(path):
        print("No specific install script found, fallback to", DEFAULT_INSTALL_SCRIPT)
        path = DEFAULT_INSTALL_SCRIPT
    return path


def _run_installer(qt_installer, show_ui, env, verbose):
    version = _get_major_minor_ver(qt_installer)
    install_script = _get_install_script(version)
    cmd = [qt_installer, "--script", install_script]
    if not show_ui:
        cmd.extend(["--platform", "minimal"])
    if verbose:
        cmd.extend(["--verbose"])
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, env=env)
    try:
        print("Running installer", cmd)
        proc.wait(INSTALL_TIMEOUT)
    except subprocess.TimeoutExpired:
        print("Timeout while waiting for the installer, kill it")
        proc.kill()
        return EXIT_ERROR
    return EXIT_OK


def _list_packages(qt_installer, show_ui):
    env = os.environ.copy()
    env["LIST_PACKAGE_ONLY"] = "1"
    return _run_installer(qt_installer, show_ui, env, verbose=True)


def _install(qt_installer, packages, destdir, show_ui, verbose, keep_tools):
    env = os.environ.copy()
    env["PACKAGES"] = packages
    env["DESTDIR"] = destdir
    ret = _run_installer(qt_installer, show_ui, env, verbose)

    if not keep_tools:
        print("Cleaning destdir")
        files = os.listdir(destdir)
        for name in files:
            fullpath = os.path.join(destdir, name)
            if re.match(r"\d+\.\d+.\d+", name):
                # Qt stands in X.Y.Z dir, skip it
                print("Keep", fullpath)
                continue
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
            else:
                os.remove(fullpath)
            print("Remove", fullpath)
    return ret


def main():
    """
    Command line tool to deploy Qt
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version", action="version", version="{} {}".format(cuteci.__application__, cuteci.__version__)
    )
    parser.add_argument("--ui", action="store_true", help="Installer UI displayed")
    parser.add_argument("--rm", action="store_true", help="Remove Qt installer")
    parser.add_argument("--installer", required=True, help="Path or url to Qt installer")

    subparsers = parser.add_subparsers(dest="action")

    subparsers.add_parser(name="list")

    install_parser = subparsers.add_parser(name="install")
    install_parser.add_argument("--packages", required=True, help="Comma separated list of package to install")
    install_parser.add_argument("--destdir", required=True, help="Path to install Qt, e.g.: /opt/Qt")
    install_parser.add_argument("--keep-tools", action="store_true", help="Keep tools, samples, doc etc")
    install_parser.add_argument("--verbose", action="store_true", help="Print debug info")

    args = parser.parse_args()

    action = args.action
    installer = args.installer
    show_ui = bool(args.ui)
    rm_installer = bool(args.rm)

    qt_installer = installer
    if installer.startswith("http"):
        qt_installer = _download_qt(installer)
    os.chmod(qt_installer, os.stat(qt_installer).st_mode | stat.S_IEXEC)

    if action == "list":
        ret = _list_packages(qt_installer, show_ui)
        status = "FAIL" if ret else "Listing OK - available packages are printed above"
    else:
        packages = args.packages
        destdir = args.destdir
        verbose = bool(args.verbose)
        keep_tools = bool(args.keep_tools)
        ret = _install(qt_installer, packages, destdir, show_ui, verbose, keep_tools)
        status = "FAIL" if ret else "Installation OK"

    if rm_installer:
        print("Removing", qt_installer)
        os.remove(qt_installer)

    print(status)
    return ret


if __name__ == "__main__":
    sys.exit(main())

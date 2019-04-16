# CuteCI

## Testing

Covered by docker and Travis CI, have a look to `test` dir if you are curious.

## Code sanity

Coding style is handled by `black` (via `ci/blackify`).
Static checks are handled by `pylint` (via `ci/pylintify`).

You must `pip3 install -r requirements/codesanity.txt` to use those scripts.

Note: continuous integration does not check code sanity.

## Release procedure

### Manually

* Bump version
* Deploy on Test PyPI

```bash
pip3 uninstall cuteci
git clean -d --force --dry-run
git clean -d --force
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip3 install --index-url https://test.pypi.org/simple/ --no-deps cuteci
cuteci --help
python3 -c "import cuteci"
```

* Deploy on PyPI

```bash
pip3 uninstall cuteci
git clean -d --force --dry-run
git clean -d --force
python3 setup.py sdist bdist_wheel
twine upload dist/*
pip3 install cuteci
cuteci --help
python3 -c "import cuteci"
```

# CuteCI

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

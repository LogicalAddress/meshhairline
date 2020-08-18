## Delete all Migration Files
```sh
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

pip install --upgrade --force-reinstall -r
```
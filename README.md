# Template


## Get Started
```
git clone https://github.com/frennkie/template
cd template
virtualenv template/venv
source template/venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

## Run Tests
```
py.test -v
```

Result should be similar to this:
```
$: py.test
================================================================================
test session starts
================================================================================
platform linux2 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2
rootdir: /home/XXX/template, inifile: setup.cfg
plugins: cache
collected 2 items

template/tests/test_misc.py .
template/tests/test_something.py .

================================================================================
2 passed in 0.05 seconds
================================================================================
```

## Customize

### Run script to change "template" to something that fits your project (not yet implemented!!)
```
./bin/start_project_from_template.sh insert_your_project_name_here
```


## Packaging
```
python setup.py sdist
```

## PEP8 (getting really funky now.. ;-) )
```
# E402 can not be passed in tests because we need to add parent dir to path
pep8 --exclude=venv --ignore=E402 .
```


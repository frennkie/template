# Template


## Getting Started

### Get and initialize template
```
git clone https://github.com/frennkie/template
cd template
virtualenv template/venv
source template/venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

### Customize

Run script to change "template" to something that fits your project (not yet implemented!!)
```
./bin/start_project_from_template.sh insert_your_project_name_here
```

## Code

Here Magic Happens (don't forget Testing, Versioning/Commiting and so on)

## Important non-coding stuff (Testing, Versioning/Git-Flow, Packaging, PEP8)

### Run Tests
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

### Versioning/Git-Flow

Versioning Style:
- Mayor Version: e.g. 0 | 1 | 2
- Minor Version: odd numbers for dev releases; even for stable releases
- Last Part: String or Number - for Hotfixes and Dev stages (e.g. 0 | 1 | dev1)

Example:
- `0.3.dev2` - unstable release; 2nd dev iteration
- `0.4.0`    - stable release 0.4
- `0.6.2`    - stable release 0.6 after 2 Hotfixes

This Style is supported by Git-Flow

http://danielkummer.github.io/git-flow-cheatsheet/

Reminders
- avoid the hotfixes.. just stick with feature branches
- if you need to create a hotfix starting from an old master/release state
  create tags manually
- the following is extremely useful for bumping version numbers in multiple
  files
```
sed -i "s/__version_info__ = ('0', '2', '0')/__version_info__ = ('0', '2', '1')/gi" *.py modules/*.py tests/*.py
```

### Packaging
```
python setup.py sdist
```

### PEP8 (getting really funky now.. ;-) )
```
# E402 can not be passed in tests because we need to add parent dir to path
pep8 --exclude=venv --ignore=E402 .
```


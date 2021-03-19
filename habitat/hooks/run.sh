#!/bin/sh

exec 2>&1

export FLASK_APP=culture_dispenser.py

echo $PYTHONPATH
pwd
ls -lrth

# cp {{pkg.path}}/*.py {{pkg.svc_path}}
# cp {{pkg.path}}/*.db {{pkg.svc_path}}

# typically let's run this from the service path
exec flask run
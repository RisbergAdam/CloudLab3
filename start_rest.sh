#!/bin/bash
celery -A CeleryWorker worker --loglevel=info &
python CeleryMaster.py &

#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

${DIR}/docker-run.sh python3 kanbandash/manage-dashboard-schema.py $@

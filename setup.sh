#!/bin/bash

YES=0
NO=1
DEBUG=$YES
VERBOSE=$YES


croak() {
    echo "ERROR $*" >&2
    kill -s TERM $BASHPID
    exit 99
}


log() {
  [[ $VERBOSE -eq $YES ]] || return
  echo "INFO $*" >&2
}


debug() {
  [[ $DEBUG -eq $YES ]] || return
  echo "DEBUG (${BASH_SOURCE[1]} [${BASH_LINENO[0]}] ${FUNCNAME[1]}) $*"
}


ensure_python() {
  [[ $DEBUG -eq $YES ]] && set -x
  PYTHON=$(which python3) 2>/dev/null
  [[ -n "$PY3_PATH" ]] && PYTHON=$PY3_PATH
  [[ -z "$PYTHON" ]] && croak "Unable to find Python3. Try setting 'PY3_PATH' env var."
  PYTHON=$( realpath -e "$PYTHON" )
  [[ -x "$PYTHON" ]] || croak "Found Python3 at '$PYTHON' but it's not executable."
  "$PYTHON" "$BASE/require_py_v3.py" || croak "Python version too low"
  "$PYTHON" -m ensurepip || croak "Something broke during ensurepip."
}


setup_python_venv() {
  [[ $DEBUG -eq $YES ]] && set -x
  venvdir="./.venv"
  [[ -d "$venvdir" ]] || {
    "$PYTHON" -m venv "$venvdir"
    PIP="$venvdir/bin/pip"
    "$PIP" install --upgrade pip
    "$PIP" install -r "$BASE/requirements.txt"
  }
  V_PYTHON="$venvdir/bin/python"
  [[ -x "$V_PYTHON" ]] || croak "Something went wrong during python venv install."
}


[[ $DEBUG -eq $YES ]] && set -x
BASE=$(readlink -e $( dirname $0 ) )

ensure_python
log "Got PYTHON: '$PYTHON'"

setup_python_venv

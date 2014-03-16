#!/bin/bash
python -mSimpleHTTPServer &
proc_pid="$!"
trap "echo 'killing server' && kill $proc_pid" SIGINT
./autocompile.py . .rst "bash build.sh"

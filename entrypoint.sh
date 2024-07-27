#!/bin/bash

sleep 10

[ -v ENVIRONMENT ] && export ENVIRONMENT=$ENVIRONMENT

if [[ ${ENVIRONMENT} = 'LOCAL' ]]; then
    exec gunicorn asgi:app -n epc-params -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 --log-level=info
else
    exec gunicorn asgi:app -n epc-params -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:5000
fi
